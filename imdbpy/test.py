import unittest
import requests


class testAPI(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/movies/"

    api = ["Inception", 'popular100', 'top250', 'bottom100', 'ind250', 'toptv', '@&#*#((@', '****$$$##']

    data = {
        "name": 'Testing',
        "description": 'Testing post functionality'
    }

    expected_result = { "title":"Interstellar", 
        "year":2014, 
        "rating":8.6, 
        "plot outline":"Earth's future has been riddled by disasters, famines, and droughts. There is only one way to ensure mankind's survival: Interstellar travel. A newly discovered wormhole in the far reaches of our solar system allows a team of astronauts to go where no man has gone before, a planet that may have the right environment to sustain human life.", 
        "genres":[ "Adventure", "Drama", "Sci-Fi" ], 
        "cast":[ "Ellen Burstyn", "Matthew McConaughey", "Mackenzie Foy", "John Lithgow", "Timoth\u00e9e Chalamet", "David Oyelowo", "Collette Wolfe", "Francis X. McCarthy", "Bill Irwin", "Anne Hathaway", "Andrew Borba", "Wes Bentley", "William Devane", "Michael Caine", "David Gyasi", "Josh Stewart", "Casey Affleck", "Leah Cairns", "Jessica Chastain", "Liam Dickinson", "Topher Grace", "Matt Damon", "Flora Nolan", "Griffen Fraser", "Jeff Hephner", "Lena Georgas", "Elyes Gabel", "Brooke Smith", "Russ Fega", "William Patrick Brown", "Cici Leah Campbell", "Mark Casimir Dyniewicz Jr.", "Troy Fyhn", "Benjamin Hardy", "Alexander Michael Helisek", "Ryan Irving", "Alexander Lu", "Derek McEntire", "Joseph Oliveira", "Benjamin Pitz", "Marlon Sanders", "Bryan Stamp", "Kristian Van der Heyden", "Kevan Weber" ], 
        "directors":[ "Christopher Nolan" ], 
        "writers":[ "Jonathan Nolan", "Christopher Nolan" ] 
    }

    def test_1_GetMovie(self):
        for i in self.api:
            resp = requests.get(self.API_URL + i)
            self.assertEqual(resp.status_code, 200)
            #self.assertEqual(len(resp.json()), 8)
            print('Test', i ,'completed!')


    # def test_2_PostMovie(self):
    #     resp = requests.post(self.URL, json = self.data)
    #     self.assertEqual(resp.status_code, 200)
    #     # self.assertDictEqual(resp.dict, self.data)
    #     print('Test 2 completed!')
    
    # def test_3_GetSpecificMovie(self):
    #     resp = requests.get(self.URL + 'movies/Interstellar')
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertDictEqual(resp.json(), self.expected_result)
    #     print('Test 3 completed!')


if __name__ == "__main__":
    tester = testAPI()

    #tester.test_1_GetMovie()
    #tester.test_2_PostMovie()
    #tester.test_3_GetSpecificMovie()
