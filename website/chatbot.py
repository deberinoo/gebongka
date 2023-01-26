from transformers import AutoModelForTokenClassification, pipeline, AutoTokenizer
import tensorflow as tf

label_names = ['B-COUGH', 'I-COUGH', 'B-BREATHLESSNESS', 'I-BREATHLESSNESS', 'B-DIZZINESS', 'I-DIZZINESS', 'B-HEADACHE', 'I-HEADACHE', 'B-CHILLS', 'I-CHILLS', 'B-CHEST_PAIN', 'I-CHEST_PAIN', 'B-BACK_PAIN', 'I-BACK_PAIN', 'B-MUSCLE_PAIN', 'I-MUSCLE_PAIN', 'B-JOINT_PAIN', 'I-JOINT_PAIN', 'B-NECK_PAIN', 'I-NECK_PAIN', 'B-STOMACH_PAIN', 'I-STOMACH_PAIN', 'O']
id2label = { i: label for i, label in enumerate(label_names) }
label2id = {v: k for k, v in id2label.items()}

my_model = AutoModelForTokenClassification.from_pretrained(
    "chatbot",
    num_labels=23,
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True
)
tokenizer = AutoTokenizer.from_pretrained("samrawal/bert-base-uncased_clinical-ner")

# instantiates a pipeline, which uses the model for inference

token_classifier = pipeline(
    "token-classification", model=my_model, 
    tokenizer=tokenizer,
    aggregation_strategy="first",
    device=0
)

text = "my back hurts!!!"
print(token_classifier(text))