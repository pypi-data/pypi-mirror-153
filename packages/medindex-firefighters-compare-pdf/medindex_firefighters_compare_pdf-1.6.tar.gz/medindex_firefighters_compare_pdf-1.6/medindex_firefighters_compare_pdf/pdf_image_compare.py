import os
from pathlib import Path
from wand.image import Image as Image
#from consts.height import HEIGHT_BOTTOM_DATE, HEIGHT_BOTTOM_FOOTNOTE, HEIGHT_PRIVATE_DATA_BLOCK
#from
from medindex_firefighters_compare_pdf.pdf_utils import get_images_from_pdf

'''ROOT_EXPECTED_DIR = os.path.abspath(os.path.join(Path(__file__).parents[1], 'expected_documents'))
EXPECTED_HEADER_PATH = os.path.join(ROOT_EXPECTED_DIR, 'headers')'''


def cut(pdf1_image, pdf2_image, crop_rectangle):
    for pdf in (pdf1_image, pdf2_image):
        if pdf:
            pdf.crop(*crop_rectangle)


def pdf_images_compare(pdf1_image, pdf2_image, diff_image_dir, diff_file_name):
    result_image, result_metric = pdf1_image.compare(pdf2_image, metric='root_mean_square')
    diff_image_name = os.path.join(diff_image_dir, diff_file_name)
    with result_image:
        result_image.save(filename=diff_image_name)
    return result_metric


class PDFImageCompare:
    '''root_dir = os.getcwd()
    download_dir = os.path.join(root_dir, 'artifacts')
    diff_image_dir = os.path.join(download_dir, 'diff_images')'''

    def __init__(self, pdf1, pdf2, expected_header, case, height_header, expected_header_path, artifacts, diff_images):
        self.artifacts = artifacts
        self.diff_images = diff_images
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
        Path(self.diff_image_dir).mkdir(parents=True, exist_ok=True)
        self.case_diff_image_dir = os.path.join(self.diff_image_dir, case)
        Path(self.case_diff_image_dir).mkdir(parents=True, exist_ok=True)
        assert os.path.exists(pdf1), f'path {pdf1} is not exist'
        assert os.path.exists(pdf2), f'path {pdf2} is not exist'
        self.pdf1 = pdf1
        self.pdf2 = pdf2
        self.expected_header = expected_header
        self.height_header = height_header
        self.expected_header_path = expected_header_path
        self.pdf1_list = get_images_from_pdf(self.pdf1)
        self.pdf2_list = get_images_from_pdf(self.pdf2)
        len_pdf1_list = len(self.pdf1_list)
        len_pdf2_list = len(self.pdf2_list)
        error_msg = f'Check FAILED: Количество страниц разное. pdf1: {len_pdf1_list}, pdf2: {len_pdf2_list}'
        assert len_pdf2_list == len_pdf1_list and len_pdf2_list != 0, error_msg

    '''@staticmethod
    def cut_bottom(pdf1_image_path, pdf2_image_path, height_bottom=HEIGHT_BOTTOM_DATE):
        w, h = pdf1_image_path.size
        w2, h2 = pdf2_image_path.size
        if w > w2:
            w = w2
        crop_rectangle = (0, 0, w, h - height_bottom)
        cut(pdf1_image_path, pdf2_image_path, crop_rectangle)

    @staticmethod
    def cut_header(pdf1_image_path, pdf2_image_path, height_header):
        w, h = pdf1_image_path.size
        w2, h2 = pdf2_image_path.size
        if w > w2:
            w = w2
        crop_rectangle = (0, height_header, w, h)
        cut(pdf1_image_path, pdf2_image_path, crop_rectangle)

    @staticmethod
    def get_header(pdf1_image_path, pdf2_image_path, height_header):
        w, h = pdf1_image_path.size
        crop_rectangle = (0, 0, w, height_header)
        cut(pdf1_image_path, pdf2_image_path, crop_rectangle)

    @staticmethod
    def get_private_data_block(pdf1_image_path, pdf2_image_path, height_private_block=HEIGHT_PRIVATE_DATA_BLOCK):
        w, h = pdf1_image_path.size
        w2, h2 = pdf2_image_path.size
        if w > w2:
            w = w2
        crop_rectangle = (0, 0, w, height_private_block)
        cut(pdf1_image_path, pdf2_image_path, crop_rectangle)

    @staticmethod
    def get_footnote(pdf1_image_path, pdf2_image_path, height_bottom=HEIGHT_BOTTOM_FOOTNOTE):
        w, h = pdf1_image_path.size
        w2, h2 = pdf2_image_path.size
        if w > w2:
            w = w2
        crop_rectangle = (0, h - height_bottom, w, h)
        cut(pdf1_image_path, pdf2_image_path, crop_rectangle)

    def get_header_diff(self):
        actual_header = self.pdf1_list[0].clone()
        self.get_header(actual_header, None, self.height_header)
        expected_header = Image(filename=(os.path.join(self.expected_header_path, self.expected_header)))
        diff_image_name = Path(self.pdf1).stem + '_header_diff.jpg'
        is_the_same_pdf = pdf_images_compare(actual_header, expected_header, self.case_diff_image_dir, diff_image_name)
        return is_the_same_pdf, diff_image_name

    def get_body_diff(self):
        compare_results = []
        count = 0
        for pdf1_img, pdf2_img in zip(self.pdf1_list, self.pdf2_list):
            results = {}
            pdf1_img = pdf1_img.clone()
            pdf2_img = pdf2_img.clone()
            self.cut_bottom(pdf1_img, pdf2_img, height_bottom=HEIGHT_BOTTOM_DATE + HEIGHT_BOTTOM_FOOTNOTE)
            self.cut_header(pdf1_img, pdf2_img, height_header=self.height_header + HEIGHT_PRIVATE_DATA_BLOCK)
            diff_image_name = Path(self.pdf1).stem + f'_body_diff_{count}.jpg'
            results['result_metric'] = pdf_images_compare(pdf1_img, pdf2_img, self.case_diff_image_dir, diff_image_name)
            results['diff_image_name'] = diff_image_name
            compare_results.append(results)
            count += 1
        return compare_results

    def get_private_data_diff(self):
        pdf1_img = self.pdf1_list[0].clone()
        pdf2_img = self.pdf2_list[0].clone()
        self.cut_header(pdf1_img, pdf2_img, self.height_header)
        self.get_private_data_block(pdf1_img, pdf2_img)
        diff_image_name = Path(self.pdf1).stem + '_private_data_diff.jpg'
        is_the_same_pdf = pdf_images_compare(pdf1_img, pdf2_img, self.case_diff_image_dir, diff_image_name)
        return is_the_same_pdf, diff_image_name

    def get_footnote_block_diff(self):
        compare_results = []
        count = 0
        for pdf1_img, pdf2_img in zip(self.pdf1_list, self.pdf2_list):
            results = {}
            pdf1_img = pdf1_img.clone()
            pdf2_img = pdf2_img.clone()
            self.cut_bottom(pdf1_img, pdf2_img, height_bottom=HEIGHT_BOTTOM_DATE)
            self.get_footnote(pdf1_img, pdf2_img)
            diff_image_name = Path(self.pdf1).stem + f'_footnote_block_diff_{count}.jpg'
            results['result_metric'] = pdf_images_compare(pdf1_img, pdf2_img, self.case_diff_image_dir, diff_image_name)
            results['diff_image_name'] = diff_image_name
            compare_results.append(results)
            count += 1
        return compare_results'''
