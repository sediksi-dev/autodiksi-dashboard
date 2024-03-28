import requests
import streamlit as st


def perform_request(endpoint):
    response = requests.get(endpoint, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get data from {endpoint}")


def check_is_wp(source):
    try:
        # Check if the site is a WordPress site
        json_endpoint = perform_request(f"https://{source}/wp-json/wp/v2")
        if not json_endpoint or json_endpoint in ["", None, False]:
            raise Exception("Situs ini bukan situs WordPress")
        posts = perform_request(f"https://{source}/wp-json/wp/v2/posts")
        if not posts or len(posts) == 0 or posts in ["", None, False]:
            raise Exception(
                "Situs adalah situs WordPress tetapi tidak memiliki postingan"
            )

        categories = perform_request(f"https://{source}/wp-json/wp/v2/categories")
        if not categories or len(categories) == 0 or categories in ["", None, False]:
            raise Exception(
                "Situs adalah situs Wordpress, tetapi tidak memiliki kategori yang dapat diambil"
            )

        return True
    except Exception as e:
        raise Exception(f"Error ketika mengecek situs: {str(e)}")


def get_example_content(endpoint):
    try:
        content = perform_request(endpoint)
        if content:
            results = [
                {
                    "id": post["id"],
                    "title": post["title"]["rendered"],
                    "content": post["content"]["rendered"],
                    "url": post["link"],
                }
                for post in content
            ]
            if results:
                return results
            else:
                raise Exception("No content available")
        else:
            raise Exception("Post type incompatible")
    except Exception as e:
        raise Exception(f"Error getting content: {str(e)}")


def check_term(source, term, count=20, page=1):
    try:
        url = f"https://{source}/wp-json/wp/v2/{term}?per_page={count}&page={page}"

        taxs = perform_request(url)
        return [
            {
                "id": tax["id"],
                "name": tax["name"],
                "total": tax["count"],
                "description": tax["description"],
                "slug": tax["slug"],
                "link": tax["link"],
            }
            for tax in taxs
        ]
    except Exception as e:
        raise Exception(f"Error checking term: {str(e)}")


def recursive_check_term(source, term, count=20, page=1):
    try:
        results = check_term(source, term, count, page)
        if results:
            return results + recursive_check_term(source, term, count, page + 1)
        else:
            return results
    except Exception as e:
        raise Exception(f"Error checking term recursively: {str(e)}")


@st.cache_data
def check_all_term(source, term):
    try:
        all_term = recursive_check_term(source, term)
        return {
            "total": len(all_term),
            "data": all_term,
        }
    except Exception as e:
        raise Exception(f"Error checking all term: {str(e)}")
