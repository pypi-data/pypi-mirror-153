import json
from urllib.request import Request, urlopen
import os

import argparse

MYJSL_ORIGIN = os.environ.get("MYJSL_ORIGIN", "https://my.johnsnowlabs.com")

# path that license should be downloaded there
LICENSE_PATH = "downloaded-license.json"
ACCESS_TOKEN = None


# using urllib to avoid additional package dependencies like requests
def http_request(url, data=None, method="POST", ACCESS_TOKEN=None):

    if data:
        data = json.dumps(data).encode("utf-8")
    request = Request(url, data=data, method=method)
    request.add_header("Authorization", f"Bearer {ACCESS_TOKEN}")
    request.add_header("Content-Type", "application/json")
    response = urlopen(request)
    status_code = response.getcode()
    return (
        json.loads(response.read().decode("utf-8"))
        if 200 <= status_code < 300
        else None
    )


def get_access_token(email, password):
    """get access token (expires in 12h)"""
    data = http_request(
        MYJSL_ORIGIN + "/graphql",
        data={
            "query": """mutation($input: LoginInput!) {
                getAccessToken(input: $input) {
                    ok {token}
                    error {
                        errors {
                          key
                          message
                        }
                    }
                }
            }""",
            "variables": {"input": {"email": email, "password": password}},
        },
    )
    if data["data"]["getAccessToken"]["error"]:
        errors = "\n".join(
            [
                error["message"]
                for error in data["data"]["getAccessToken"]["error"]["errors"]
            ]
        )
        print(f"Cannot login. error={errors}")
        exit(1)
    access_token = data["data"]["getAccessToken"]["ok"]["token"]
    return access_token


def get_user_licenses(ACCESS_TOKEN):
    licenses_query = """query LicensesQuery {
  licenses(isValid: true, platforms: ["Airgap", "Floating"]) {
    edges {
      node {
        id
        type
        endDate
        platform {
          name
          type
        }
        products {
          name
        }
      }
    }
  }
}
 """
    data = http_request(f"{MYJSL_ORIGIN}/graphql", {"query": licenses_query}, ACCESS_TOKEN=ACCESS_TOKEN)
    if data:
        if "errors" in data:
            raise Exception("Invalid or Expired token.")
        licenses = [s["node"] for s in data["data"]["licenses"]["edges"]]
    else:
        raise Exception("Something went wrong...")
    return licenses


def download_license(license, ACCESS_TOKEN):
    print("Downloading license...")
    data = http_request(
        "{}/attachments/{}".format(MYJSL_ORIGIN, license["id"]), method="GET",
        ACCESS_TOKEN=ACCESS_TOKEN
    )
    if data:
        # TODO store in ~/jsl home!!
        # json.dump(data, open(LICENSE_PATH, "w"))
        # print("Licenses extracted successfully")
        return data
    else:
        raise Exception(f"Failed fetching license.")





def ensure_correct_choice(licenses_count):
    license_id = input()
    if license_id.isnumeric():
        index = int(license_id) - 1
        if licenses_count > index:
            return index
        else:
            print(f"Please select value between 1 and {licenses_count}")
            return ensure_correct_choice(licenses_count)
    else:
        print(f"Please select value between 1 and {licenses_count}")
        return ensure_correct_choice(licenses_count)


def get_user_license_choice(licenses):
    print("Please select the license to use.")
    for idx, license in enumerate(licenses):
        products = ",".join(s["name"] for s in license["products"])
        if license["platform"] is None:
            scope = "Airgap"
        else:
            scope = license["platform"]["name"]
            type = license["platform"]["type"]
            if scope == "Floating":
                if type:
                    scope = scope + "," + type.capitalize()

        print(
            "{}. Libraries: {}\n   License Type: {}\n   Expiration Date: {}\n   Scope: {}".format(
                idx + 1, products, license["type"], license["endDate"], scope
            )
        )

    choice = ensure_correct_choice(len(licenses))
    return licenses[choice]


# if __name__ == "__main__":
#         # get token from acces
#         # ACCESS_TOKEN = get_access_token(args.email, password)
#         # get available licenses
#         licenses = get_user_licenses(ACCESS_TOKEN)
#         # if more than once license, show options
#     if len(licenses) == 0:
#         raise Exception(
#             f"It seems there are no compatible licenses available. Please request a license first using {MYJSL_ORIGIN}"
#         )
#     if len(licenses) == 1:
#         license_to_use = licenses[0]
#     else:
#         license_to_use = get_user_license_choice(licenses)
#     # download license to file
#     download_license(license_to_use)
# except Exception as e:
#     print(e)
#     exit(1)
