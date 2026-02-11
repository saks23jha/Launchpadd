from src.retriever.image_search import text_to_image, image_to_text

def ask_image(query: str):
    scores, idxs = text_to_image(query)

    return {
        "query": query,
        "results": [
            {"image_index": int(i), "score": float(s)}
            for i, s in zip(idxs, scores)
        ]
    }


def explain_image(image_path: str):
    caption, ocr = image_to_text(image_path)
    return {
        "image": image_path,
        "caption": caption,
        "ocr_text": ocr[:500]
    }
