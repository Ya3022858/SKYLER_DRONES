import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

class MondayClient:
    def __init__(self):
        self.api_key = os.getenv("MONDAY_API_KEY")
        self.api_url = "https://api.monday.com/v2"
        self.headers = {
            "Authorization": self.api_key,
            "API-Version": "2023-10"
        }

    def execute_query(self, query, variables=None):
        if not self.api_key:
            raise ValueError("Monday API Key not found. Please set MONDAY_API_KEY in .env file.")

        data = {"query": query, "variables": variables}
        response = requests.post(self.api_url, json=data, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Monday API Error: {response.text}")
            
        json_response = response.json()
        
        if "errors" in json_response:
             raise Exception(f"GraphQL Errors: {json_response['errors']}")
             
        return json_response

    def get_board_items(self, board_id):
        """
        Fetches all items from a board using cursor-based pagination.
        """
        all_items = []
        cursor = None
        
        while True:
            if cursor:
                query = """
                query ($board_id: [ID!], $cursor: String) {
                    boards (ids: $board_id) {
                        items_page (cursor: $cursor, limit: 500) {
                            cursor
                            items {
                                id
                                name
                                column_values {
                                    id
                                    text
                                    value
                                    type
                                }
                            }
                        }
                    }
                }
                """
                variables = {"board_id": [board_id], "cursor": cursor}
            else:
                query = """
                query ($board_id: [ID!]) {
                    boards (ids: $board_id) {
                        items_page (limit: 500) {
                            cursor
                            items {
                                id
                                name
                                column_values {
                                    id
                                    text
                                    value
                                    type
                                }
                            }
                        }
                    }
                }
                """
                variables = {"board_id": [board_id]}

            response = self.execute_query(query, variables)
            
            # Navigate the nested response structure safely
            try:
                boards = response["data"]["boards"]
                if not boards:
                    break
                
                items_page = boards[0]["items_page"]
                all_items.extend(items_page["items"])
                cursor = items_page["cursor"]
                
                if not cursor:
                    break
            except (KeyError, IndexError, TypeError) as e:
                print(f"Error parsing response: {e}")
                break
                
        return all_items

    def get_board_columns(self, board_id):
        """
        Fetches column definitions for a board.
        Returns a dictionary mapping column ID to column Title.
        """
        query = """
        query ($board_id: [ID!]) {
            boards (ids: $board_id) {
                columns {
                    id
                    title
                    type
                }
            }
        }
        """
        variables = {"board_id": [board_id]}
        response = self.execute_query(query, variables)
        
        columns_map = {}
        try:
            columns = response["data"]["boards"][0]["columns"]
            for col in columns:
                columns_map[col["id"]] = col["title"]
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error parsing columns response: {e}")
            
        return columns_map
