class FakeModel:

    @staticmethod
    def get_kata():
        return ['Хейан Нидан', 'Kata2']

    @staticmethod
    def process(kata : str, video_path : str):

        return [
            {
                'id': 1,
                'name': 'Рэй',
                'photo': '1.jpg',
                'video': None,
                'completed': True,
                'score': 7,
            },
            {
                'id': 2,
                'name': 'Ёй',
                'photo': '2.jpg',
                'video': None,
                'completed': True,
                'score': 7,
            },
            {
                'id': 3,
                'name': 'Кокутсу дачи',
                'photo': None,
                'video': None,
                'completed': False,
                'score': 0,
            }
        ]

