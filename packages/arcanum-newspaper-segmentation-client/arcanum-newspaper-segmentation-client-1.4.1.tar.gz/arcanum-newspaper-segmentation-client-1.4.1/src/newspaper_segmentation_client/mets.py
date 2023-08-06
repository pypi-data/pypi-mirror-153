import os
from datetime import datetime
from typing import List, Tuple

from xml.etree.ElementTree import ElementTree, Element, SubElement

from PIL import Image


class MetsConverter:
    def __init__(self):
        pass

    @staticmethod
    def _get_articles(segmentation_result):
        return segmentation_result["articles"]

    @staticmethod
    def _get_blocks_from_articles(article):
        return article["blocks"]

    @staticmethod
    def _get_bounds(block) -> Tuple[int, int, int, int]:
        return block["bounds"]

    @staticmethod
    def _get_content(block) -> str:
        return block["content"]

    @staticmethod
    def _get_label(block) -> str:
        return block["label"]

    def _get_article_title(self, article):
        title = ""
        for block in self._get_blocks_from_articles(article):
            if self._get_label(block) != "Title":
                if title:
                    break
                continue
            if title:
                title += " "
            title += self._get_block_text(block)
        return title

    @staticmethod
    def _convert_textract_bounds(textract_bounds: dict, width: int, height: int) -> Tuple[int, int, int, int]:
        return (textract_bounds["Left"] * width,
                textract_bounds["Top"] * height,
                (textract_bounds["Left"] + textract_bounds["Width"]) * width,
                (textract_bounds["Top"] + textract_bounds["Height"]) * height)

    @staticmethod
    def _get_block_text(block):
        text = ""
        for textract_block in block["ocr_blocks"]:
            if textract_block['BlockType'] != 'WORD':
                continue
            if text:
                text += " "
            text += textract_block["Text"]
        return text

    def _get_ocr_blocks(self, block, width: int, height: int) -> Tuple[List, List]:
        lines = []
        child_ids = {}
        for textract_block in block["ocr_blocks"]:
            if textract_block['BlockType'] == 'LINE':
                line_dict = {
                    "bounds": self._convert_textract_bounds(textract_block["Geometry"]["BoundingBox"], width, height)
                }
                lines.append(line_dict)
                for relation in textract_block["Relationships"]:
                    if relation["Type"] == "CHILD":
                        for word_id in relation["Ids"]:
                            child_ids[word_id] = len(lines) - 1

        words = [[] for _ in range(len(lines))]
        for textract_block in block["ocr_blocks"]:
            if textract_block['BlockType'] == 'WORD':
                word_dict = {
                    "bounds": self._convert_textract_bounds(textract_block["Geometry"]["BoundingBox"], width, height),
                    "content": textract_block["Text"]
                }
                line_idx = child_ids[textract_block["Id"]]
                words[line_idx].append(word_dict)
        return lines, words

    def _get_article_type(self, article):
        blocks = self._get_blocks_from_articles(article)
        block_count = len(blocks)
        advertising_count = len([block for block in blocks if self._get_label(block) == "Advertising"])
        artifact_count = len([block for block in blocks if self._get_label(block) == "Artifact"])
        if advertising_count > block_count // 2:
            return "Advertising"
        if artifact_count > block_count // 2:
            return "Artifact"
        return "Editorial Content"

    @staticmethod
    def _bounds_coords(bounds: Tuple[int, int, int, int]) -> str:
        bounds = str(int(round(bounds[0]))), str(int(round(bounds[1]))), \
                 str(int(round(bounds[2]))), str(int(round(bounds[3])))
        return " ".join(bounds)

    @staticmethod
    def _bounds_to_alto(bounds: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
        return bounds[0], bounds[1], bounds[2] - bounds[0], bounds[3] - bounds[1]

    def _bounds_params(self, bounds: Tuple[int, int, int, int]) -> dict:
        hpos, vpos, width, height = self._bounds_to_alto(bounds)
        return {"HPOS": str(int(round(hpos))), "VPOS": str(int(round(vpos))),
                "HEIGHT": str(int(round(height))), "WIDTH": str(int(round(width)))}

    def _create_alto_base_tags(self, width: int, height: int) -> Tuple[Element, Element]:
        root = Element("alto", {"xmlns": "http://www.loc.gov/standards/alto/ns-v2#",
                                "xmlns:xlink": "http://www.w3.org/1999/xlink",
                                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                                "schemaLocation": "http://www.loc.gov/standards/alto/ns-v2# "
                                                  "http://www.loc.gov/standards/alto/alto-v2.0.xsd"})
        description = SubElement(root, 'Description')
        measurement_unit = SubElement(description, 'MeasurementUnit')
        measurement_unit.text = "pixel"
        layout = SubElement(root, 'Layout')
        page = SubElement(layout, 'Page', {'ID': 'Page', 'PHYSICAL_IMG_NR': '1',
                                           'HEIGHT': str(height), 'WIDTH': str(width)})
        print_space_params = self._bounds_params((0, 0, width, height))
        print_space_params["ID"] = "SP_1"
        print_space = SubElement(page, 'PrintSpace', print_space_params)
        return root, print_space

    @staticmethod
    def _convert_bounds(bounds: Tuple[int, int, int, int], width, height):
        return bounds[0] * width, bounds[1] * height, bounds[2] * width, bounds[3] * height

    def _create_text_block_element(self, parent: Element, identifier: str, bounds: Tuple[int, int, int, int],
                                   width: int, height: int) -> Element:
        bounds = self._convert_bounds(bounds, width, height)
        params = self._bounds_params(bounds)
        params["ID"] = identifier
        return SubElement(parent, 'TextBlock', params)

    def _create_text_line_element(self, parent: Element, identifier: str, bounds: Tuple[int, int, int, int]) \
            -> Element:
        params = self._bounds_params(bounds)
        params["ID"] = identifier
        return SubElement(parent, 'TextLine', params)

    def _create_string_element(self, parent: Element, identifier: str, bounds: Tuple[int, int, int, int], content) \
            -> Element:
        params = self._bounds_params(bounds)
        params["ID"] = identifier
        params["CONTENT"] = content
        return SubElement(parent, 'String', params)

    def _create_alto_blocks(self, segmentation_response, print_space: Element, width: int, height: int):
        block_idx = 1
        line_idx = 1
        word_idx = 1
        for article in self._get_articles(segmentation_response):
            for block in self._get_blocks_from_articles(article):
                text_block = self._create_text_block_element(parent=print_space, identifier=f'SP_1_TB{block_idx:05d}',
                                                             bounds=self._get_bounds(block), width=width, height=height)
                block_idx += 1
                lines, line_words = self._get_ocr_blocks(block, width, height)
                for line, words in zip(lines, line_words):
                    text_line = self._create_text_line_element(parent=text_block, identifier=f'SP_1_TL{line_idx:05d}',
                                                               bounds=self._get_bounds(line))
                    line_idx += 1
                    for word in words:
                        self._create_string_element(parent=text_line, identifier=f'SP_1_ST{word_idx:05d}',
                                                    bounds=self._get_bounds(word), content=self._get_content(word))
                        word_idx += 1

    def _pretty_print(self, current, parent=None, index=-1, depth=0):
        for i, node in enumerate(current):
            self._pretty_print(node, current, i, depth + 1)
        if parent is not None:
            if index == 0:
                parent.text = '\n' + ('  ' * depth)
            else:
                parent[index - 1].tail = '\n' + ('  ' * depth)
            if index == len(parent) - 1:
                current.tail = '\n' + ('  ' * (depth - 1))

    def _save_xml(self, root_tag: Element, output_path: str):
        self._pretty_print(root_tag)
        tree = ElementTree(root_tag)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def _date_xml(date: datetime) -> str:
        return date.strftime("%Y-%m-%dT%H:%M:%S")

    def convert_segmentation_result_to_alto(self, segmentation_response, alto_output_path: str, width: int,
                                            height: int):
        root, print_space = self._create_alto_base_tags(width, height)
        self._create_alto_blocks(segmentation_response, print_space, width, height)
        self._save_xml(root, alto_output_path)

    @staticmethod
    def rotate_and_save_image(image: Image, rotation: float, output: str):
        if rotation != 0.0:
            image = image.rotate(-rotation, expand=True)
        image.save(output)

    def _create_mets_base_tags(self):
        mets_root = Element("METS:mets", {
            "xmlns:METS": "http://www.loc.gov/METS/",
            "xmlns:mets": "http://www.loc.gov/METS/",
            "xmlns:mix": "http://www.loc.gov/mix/v20",
            "xmlns:mods": "http://www.loc.gov/mods/v3",
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "OBJID": "#OBJID#",
            "PROFILE": "ENMAP",
            "TYPE": "unknown",
            "xsi:schemaLocation": "http://www.loc.gov/METS/ http://www.loc.gov/standards/mets/version191/mets.xsd "
                                  "http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/mods.xsd "
                                  "http://www.loc.gov/mix/v20 http://www.loc.gov/standards/mix/mix20/mix20.xsd"
        })
        now = datetime.now()
        mets_header = SubElement(mets_root, "mets:metsHdr", {
            "CREATEDATE": self._date_xml(now),
            "LASTMODDATE": self._date_xml(now),
            "RECORDSTATUS": "SUBMITTED"
        })
        mets_agent = SubElement(mets_header, "mets:agent", {
            "ROLE": "CREATOR",
            "TYPE": "ORGANIZATION"
        })
        mets_agent_name = SubElement(mets_agent, "mets:name")
        mets_agent_name.text = "Arcanum Ltd. (https://www.arcanum.com)"
        return mets_root

    @staticmethod
    def _create_file_section(mets_root, image_count):
        file_sec = SubElement(mets_root, "mets:fileSec")
        image_group = SubElement(file_sec, "mets:fileGrp", {"USE": "Preservation"})
        alto_group = SubElement(file_sec, "mets:fileGrp", {"USE": "Content"})
        for image_idx in range(image_count):
            image_file = SubElement(image_group, "mets:file",
                                    {"ID": f"FID-{image_idx:04d}-OCRMASTER", "SEQ": str(image_idx + 1)})
            SubElement(image_file, "mets:FLocat", {"LOCTYPE": "URL", "xlink:href": f"file:///./{image_idx:04d}.jpg"})
            alto_file = SubElement(alto_group, "mets:file",
                                   {"ID": f"FID-{image_idx:04d}-ALTO", "SEQ": str(image_idx + 1)})
            SubElement(alto_file, "mets:FLocat", {"LOCTYPE": "URL", "xlink:href": f"file:///./{image_idx:04d}.xml"})

    @staticmethod
    def _create_struct_map(mets_root, image_count):
        struct_map = SubElement(mets_root, "mets:structMap", {"LABEL": "Physical Structure", "TYPE": "PHYSICAL"})
        mets_div = SubElement(struct_map, "mets:div",
                              {"DMDID": "MODS_1", "ID": "physb1", "ORDER": "1", "TYPE": "physSequence"})

        for image_idx in range(image_count):
            order = image_idx + 1
            div_params = {"ID": f"phys{order}", "ORDER": str(order), "ORDERLABEL": str(order), "TYPE": "page"}
            mets_sub_div = SubElement(mets_div, "mets:div", div_params)
            SubElement(mets_sub_div, "mets:fptr", {"FILEID": f"FID-{image_idx:04d}-OCRMASTER"})
            SubElement(mets_sub_div, "mets:fptr", {"FILEID": f"FID-{image_idx:04d}-ALTO"})

    @staticmethod
    def _create_logical_structure_base(parent):
        struct_map = SubElement(parent, "mets:structMap", {"ID": "Logical_Structure", "TYPE": "logical_structmap"})
        return SubElement(struct_map, "mets:div", {"DMDID": "MODS_1", "ID": "LSB1", "LABEL": "", "ORDER": "1",
                                                   "TYPE": "Newspaper"})

    def _create_article_metadata(self, article_idx, article, parent):
        dmd_sec = SubElement(parent, "mets:dmdSec", {"ID": f"DMD_LS{article_idx}"})
        md_wrap = SubElement(dmd_sec, "mets:mdWrap", {"MDTYPE": "MODS"})
        xml_data = SubElement(md_wrap, "mets:xmlData")
        mods = SubElement(xml_data, "mods:mods")

        article_type = self._get_article_type(article)
        subject = SubElement(mods, "mods:subject")
        topic = SubElement(subject, "mods:topic")
        topic.text = article_type

        article_title = self._get_article_title(article)
        title_info = SubElement(mods, "mods:titleInfo")
        title = SubElement(title_info, "mods:title")
        title.text = article_title

    def _create_article(self, image_idx, article_idx, div_idx, article, parent, width, height):
        article_title = self._get_article_title(article)
        article_params = {"DMDID": f"DMD_LS{article_idx}", "ID": f"LSA{article_idx}", "LABEL": article_title,
                          "ORDER": str(article_idx), "TYPE": "contentUnit"}
        article_div = SubElement(parent, "mets:div", article_params)
        block_order = 1
        for block in self._get_blocks_from_articles(article):
            block_params = {"ID": f"LS{div_idx}", "ORDER": str(block_order), "TYPE": self._get_label(block)}
            block_div = SubElement(article_div, "mets:div", block_params)
            image_fptr = SubElement(block_div, "mets:fptr")

            block_coords = self._bounds_coords(self._convert_bounds(self._get_bounds(block), width, height))
            SubElement(image_fptr, "mets:area", {"FILEID": f"FID-{image_idx:04d}-OCRMASTER", "COORDS": block_coords})
            alto_fptr = SubElement(block_div, "mets:fptr")
            SubElement(alto_fptr, "mets:area", {"FILEID": f"FID-{image_idx:04d}-ALTO", "COORDS": block_coords})
            block_order += 1
            div_idx += 1
        return div_idx

    @staticmethod
    def _create_ls_root(mets_root):
        dmd_sec = SubElement(mets_root, "mets:dmdSec", {"ID": "MODS_1"})
        md_wrap = SubElement(dmd_sec, "mets:mdWrap", {"MDTYPE": "MODS"})
        xml_data = SubElement(md_wrap, "mets:xmlData")
        mods = SubElement(xml_data, "mods:mods")
        title_info = SubElement(mods, "mods:titleInfo")
        title = SubElement(title_info, "mods:title")
        title.text = "Newspaper issue"

    def convert_segmentation_results_to_mets(self, images: List[str], segmentation_responses: List, output_dir: str):
        assert len(images) == len(segmentation_responses)

        mets_root = self._create_mets_base_tags()
        self._create_file_section(mets_root, len(images))
        self._create_struct_map(mets_root, len(images))
        self._create_ls_root(mets_root)
        logical_structure = self._create_logical_structure_base(mets_root)
        article_idx = 1
        div_idx = 1

        for image_idx in range(len(images)):
            image = Image.open(images[image_idx])
            segmentation_response = segmentation_responses[image_idx]

            alto_output_path = os.path.join(output_dir, f"{image_idx:04d}.xml")
            self.convert_segmentation_result_to_alto(segmentation_response, alto_output_path, image.width, image.height)

            image_output_path = os.path.join(output_dir, f"{image_idx:04d}.jpg")
            self.rotate_and_save_image(image, segmentation_response["rotation"], image_output_path)

            for article in self._get_articles(segmentation_response):
                self._create_article_metadata(article_idx, article, mets_root)
                div_idx = self._create_article(image_idx, article_idx, div_idx, article, logical_structure,
                                               image.width, image.height)
                article_idx += 1

        mets_output_path = os.path.join(output_dir, "mets.xml")
        self._save_xml(mets_root, mets_output_path)
