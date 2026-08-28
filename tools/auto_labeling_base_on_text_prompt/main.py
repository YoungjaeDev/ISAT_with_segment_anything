# -*- coding: utf-8 -*-
# @Author  : LG

from PIL import Image
from segment_any.segment_any import SegAny
import cv2
import numpy as np
import os
from json import dump, load
from typing import List, Union
from pathlib import Path
from tqdm import tqdm
import warnings


class Object:
    r"""A class to represent an annotation object.

    Arguments:
        category (str): The category of the object.
        group (int): The group of the object.
        segmentation (list | tuple): The vertices of the object.[(x1, y1), (x2, y2), ...]
        area (float): The area of the object.
        layer (int): The layer of the object.
        bbox (list | tuple): The bbox of the object. [xmin, ymin, xmax, ymax]
        iscrowd (bool): The crowd tag of the object.
        note (str): The note of the object.
    """

    def __init__(
        self,
        category: str,
        group: int,
        segmentation: Union[list, tuple],
        area: float,
        layer: int,
        bbox: Union[list, tuple],
        iscrowd: bool = False,
        note: str = "",
        is_obb: bool = False,
    ):
        self.category = category
        self.group = group
        self.segmentation = segmentation
        self.area = area
        self.layer = layer
        self.bbox = bbox
        self.iscrowd = iscrowd
        self.note = note
        self.is_obb = is_obb


class Annotation:
    r"""A class to represent an annotation containing many objects.

    Arguments:
        image_path (str): The path to the image.
        label_path (str): The path to the label file.

    Attributes:
        description (str): Always 'ISAT'.
        img_folder (str): The path to the folder where the images are located.
        img_name (str): The name of the image.
        label_path (str): The path to the label file.
        note (str): The note of the image.
        height (int): The height of the image.
        width (int): The width of the image.
        depth (int): The depth of the image.
    """

    def __init__(self, image_path: str, label_path: str):
        img_folder, img_name = os.path.split(image_path)
        self.description = "ISAT"
        self.img_folder = img_folder
        self.img_name = img_name
        self.label_path = label_path
        self.note = ""

        image = np.array(Image.open(image_path))
        if image.ndim == 3:
            self.height, self.width, self.depth = image.shape
        elif image.ndim == 2:
            self.height, self.width = image.shape
            self.depth = 0
        else:
            print(
                "Warning: Except image has 2 or 3 ndim, but get {}.".format(image.ndim)
            )
            # shape 는 튜플이라 2차원 슬라이스를 받지 못한다. 앞 3개 축만 쓴다
            self.height, self.width, self.depth = image.shape[:3]
        del image

        self.objects: List[Object,] = []

    def load_annotation(self):
        r"""
        Load annotation from self.label_path
        """
        if os.path.exists(self.label_path):
            with open(self.label_path, "r", encoding="utf-8") as f:
                dataset = load(f)
                info = dataset.get("info", {})
                description = info.get("description", "")
                if description == "ISAT":
                    # ISAT格式json
                    objects = dataset.get("objects", [])
                    self.img_name = info.get("name", "")
                    width = info.get("width", None)
                    if width is not None:
                        self.width = width
                    height = info.get("height", None)
                    if height is not None:
                        self.height = height
                    depth = info.get("depth", None)
                    if depth is not None:
                        self.depth = depth
                    self.note = info.get("note", "")
                    for obj in objects:
                        category = obj.get("category", "unknow")
                        group = obj.get("group", 0)
                        if group is None:
                            group = 0
                        segmentation = obj.get("segmentation", [])
                        iscrowd = obj.get("iscrowd", False)
                        iscrowd = (
                            iscrowd if isinstance(iscrowd, bool) else bool(iscrowd)
                        )
                        note = obj.get("note", "")
                        area = obj.get("area", 0)
                        layer = obj.get("layer", 2)
                        bbox = obj.get("bbox", [])
                        is_obb = obj.get("is_obb", False)
                        obj = Object(
                            category,
                            group,
                            segmentation,
                            area,
                            layer,
                            bbox,
                            iscrowd,
                            note,
                            is_obb,
                        )
                        self.objects.append(obj)
                else:
                    # 不再支持直接打开labelme标注文件（在菜单栏-tool-convert中提供了isat<->labelme相互转换工具）
                    print(
                        "Warning: The file {} is not a ISAT json.".format(
                            self.label_path
                        )
                    )
        return self

    def save_annotation(self):
        r"""
        Save annotation to self.label_path
        """
        dataset = {}
        dataset["info"] = {}
        dataset["info"]["description"] = self.description
        dataset["info"]["folder"] = self.img_folder
        dataset["info"]["name"] = self.img_name
        dataset["info"]["width"] = self.width
        dataset["info"]["height"] = self.height
        dataset["info"]["depth"] = self.depth
        dataset["info"]["note"] = self.note
        dataset["objects"] = []
        for obj in self.objects:
            object = {}
            object["category"] = obj.category
            object["group"] = obj.group
            object["segmentation"] = obj.segmentation
            object["area"] = obj.area
            object["layer"] = obj.layer
            object["bbox"] = obj.bbox
            object["iscrowd"] = obj.iscrowd
            object["note"] = obj.note
            object["is_obb"] = obj.is_obb
            dataset["objects"].append(object)
        with open(self.label_path, "w", encoding="utf-8") as f:
            dump(dataset, f, indent=4, ensure_ascii=False)
        return True


def mask_to_polygon(mask: np.ndarray):
    mask = mask.astype("uint8") * 255
    h, w = mask.shape[-2:]
    mask = mask.reshape(h, w)

    contour_method = cv2.CHAIN_APPROX_SIMPLE


    # 当只保留外轮廓或单个mask时，只检测外轮廓
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, contour_method
    )

    if contours:
        largest_contour = max(
            contours, key=cv2.contourArea
        )  # 只保留面积最大的轮廓
        contours = [largest_contour]

    # polydp
    epsilon_factor = 0.001
    polydp_contours = []
    for contour in contours:
        epsilon = epsilon_factor * cv2.arcLength(contour, True)
        contour = cv2.approxPolyDP(contour, epsilon, True)
        polydp_contours.append(contour)
    contours = polydp_contours

    return contours, hierarchy


def text_prompt_and_save_to_isat_json(segany, prompts, images_root):
    images_root = Path(images_root)
    bar = tqdm(images_root.iterdir())
    for image_path in bar:
        if image_path.suffix != ".jpg":
            continue
        label_path = image_path.with_suffix(".json")

        try:
            # 新建标注类
            anno = Annotation(image_path=image_path, label_path=label_path)

            # 预测
            image = Image.open(image_path).convert("RGB")
            group = 0
            for prompt in prompts:
                masks, scores = segany.predictor.predict_with_text_prompt(image, prompt)

                num_masks = len(scores)
                bar.set_description(f"{prompt} - {num_masks} - {image_path.name}")

                for i in range(num_masks):
                    # mask转轮廓
                    contours, hierarchy = mask_to_polygon(masks[i])
                    # 빈 마스크면 윤곽이 없다. 여기서 죽으면 바깥 except 가 잡아
                    # save_annotation 을 건너뛰므로 이 이미지의 나머지 결과까지 잃는다
                    if not contours:
                        continue
                    contour = contours[0]

                    # 轮廓转polygon顶点
                    segmentation = []
                    for point in contour:
                        x, y = point[0]
                        x = max(0.1, x)
                        y = max(0.1, y)
                        segmentation.append([int(x), int(y)])

                    # 新建目标
                    # group 은 ISAT 인스턴스 ID 라서 검출 결과마다 달라야 한다.
                    # 상수로 두면 COCO/YOLO 내보내기가 같은 카테고리를 하나로 합친다.
                    group += 1
                    xs = [point[0] for point in segmentation]
                    ys = [point[1] for point in segmentation]
                    obj = Object(category=prompt, group=group, segmentation=segmentation,
                                 area=float(cv2.contourArea(contour)), layer=0,
                                 bbox=[min(xs), min(ys), max(xs), max(ys)], iscrowd=False,
                                 note="", is_obb=False)
                    # 添加目标
                    anno.objects.append(obj)
            # 保存
            anno.save_annotation()
        except Exception as e:
            warnings.warn(f"Error | {image_path.name}: {e}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="使用文本提示词调用SAM3模型，对图片目录中的图片进行自动分割，生成ISAT格式的标注JSON文件。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-c", "--checkpoint", type=str, required=True,
        help="SAM3模型权重文件的路径（如 sam3.pt）。",
    )
    parser.add_argument(
        "-p", "--prompts", type=str, nargs="+", required=True,
        help="一个或多个文本提示词（如 'dog' 'cat'），每个提示词对应一个目标类别。",
    )
    parser.add_argument(
        "-i", "--image_root", type=str, required=True,
        help="待标注图片所在的目录路径，脚本会遍历目录下所有 .jpg 图片。",
    )
    args = parser.parse_args()

    assert "sam3.pt" in args.checkpoint, "The checkpoint must be sam3.pt"

    segany = SegAny(args.checkpoint, use_bfloat16=False)

    text_prompt_and_save_to_isat_json(segany, args.prompts, args.image_root)

