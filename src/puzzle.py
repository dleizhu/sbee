import requests
from bs4 import BeautifulSoup

class Puzzle:

    def __init__(self, puzzle_num=1):
        url_tail = "answers" if puzzle_num == 0 else f"s/{puzzle_num}"
        url = "https://www.sbsolver.com/" + url_tail
        self.letters, self.word_points = self.parse_url(url)
    
    def parse_url(self, url):
        """
        Scrape the letters and word answers from the given sbsolver URL.

        Args:
            url (string): The URL to a sbsolver day
        Returns:
            [<letters for the day (string)>, <word answers and point values (dict)>]
        
        Example:
            >>> parse_url(https://www.sbsolver.com/s/1)
            "Wahorty", {"ARROW":5, ..., "YARROW":6}
        """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        letters_element = soup.find(id="string")
        letters_str = letters_element["value"]

        word_elements = soup.find_all("td", class_="bee-hover")
        word_points = {}
        for word_elem in word_elements:
            word_points[word_elem.text] = self.calc_word_points(word_elem)
        return letters_str, word_points

    def calc_word_points(self, word_elem):
        """
        Calculate the number of points a word is worth. Four-letter words are worth
        1 point. Words that are five letters or longer earn one point per letter. 
        Pangrams earn an additional 7 points.
        
        Args:
            word_elem (BeautifulSoup): An HTML element for a word answer
        Returns:
            Number of points the word is worth (int)
        
        Example:
            >>> calc_word_points(<HTML element for word "AWAY">)
            1
            >>> calc_word_points(<HTML element for word "ARROW">)
            5
            >>> calc_word_points(<HTML element for word "THROWAWAY") # a pangram
            16
        """
        word_len = len(word_elem.text)
        if word_len == 4:
            points = 1
        elif word_len > 4:
            points = word_len
            is_pangram = is_pangram = bool(word_elem.parent.find("td", class_="bee-note"))
            if is_pangram:
                points += 7
        return points

    def print(self):
        print("letters: " + self.letters)
        print("word points:")
        print(self.word_points)