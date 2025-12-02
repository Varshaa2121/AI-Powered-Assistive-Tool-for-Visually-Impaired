from paddleocr import PaddleOCR as __Reader
from transformers import pipeline as __pipe

__ocr_engine = __Reader(lang='en')
__summarizer = __pipe("summarization")

def __extract(__img):
    out = __ocr_engine.ocr(__img)
    return " ".join([txt[1][0] for txt in out[0]]) if out else ""

def __summarize(content, __limit=100):
    result = __summarizer(content, max_length=__limit, min_length=30, do_sample=False)
    return result[0]['summary_text'] if result else ""

def analyze_image(path_to_img):
    __raw = __extract(path_to_img)
    print("\nFetched Text:\n", __raw)

    if len(__raw.strip()) > 50:
        __short = __summarize(__raw)
        print("\nCompressed Summary:\n", __short)
    else:
        print("\nBrief content — no summary generated.")

# Sample call (remove/comment in production)
if __name__ == "__main__":
    analyze_image("sample.jpg")
