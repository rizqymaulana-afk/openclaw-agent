# memory_extractor.py

class MemoryExtractor:

    def extract(self, user_input):

        user_input_lower = user_input.lower().strip()

        # jangan extract kalau pertanyaan
        if "?" in user_input_lower:

            return None

        # save user name
        if user_input_lower.startswith(
            "nama saya"
        ):

            name = user_input_lower.replace(
                "nama saya",
                ""
            ).strip()

            if name:

                return {
                    "type": "fact",
                    "key": "name",
                    "value": name
                }

        # favorite
        if user_input_lower.startswith(
            "saya suka"
        ):

            thing = user_input_lower.replace(
                "saya suka",
                ""
            ).strip()

            if thing:

                return {
                    "type": "fact",
                    "key": "favorite",
                    "value": thing
                }

        # job
        if user_input_lower.startswith(
            "saya bekerja sebagai"
        ):

            job = user_input_lower.replace(
                "saya bekerja sebagai",
                ""
            ).strip()

            if job:

                return {
                    "type": "fact",
                    "key": "job",
                    "value": job
                }

        # city
        if user_input_lower.startswith(
            "saya tinggal di"
        ):

            city = user_input_lower.replace(
                "saya tinggal di",
                ""
            ).strip()

            if city:

                return {
                    "type": "fact",
                    "key": "city",
                    "value": city
                }

        return None