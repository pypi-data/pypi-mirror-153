import yaml
from qary.config import DATA_DIR
from pathlib import Path


def load_db(
        filepath=Path(DATA_DIR) / 'book_smarts' / 'book_club_discussion_question_templates.yml'):
    return yaml.full_load(Path(filepath).open())


def titlize(title):
    return '_' + str(title).strip().title() + '_'


def generate_questions(db):
    generated_questions = []
    db = load_db()
    for book in db['books']:
        book['The_book'] = titlize(book['title'])
        book['the_book'] = book['The_book']
        book['author_pronoun'] = 'they'
        book['author_full_name'] = '*' + book['author'].strip().title() + '*'

    for question in db['questions']:
        for book in db['books']:
            if book['title'] in question.get('example_titles', []):
                generated_questions.append(question['template'].format(**book))
    return generated_questions


if __name__ == '__main__':
    questions = generate_questions()
    for q in questions:
        print(q)
