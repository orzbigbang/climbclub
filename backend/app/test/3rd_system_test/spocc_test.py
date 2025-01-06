"""
HOW TO USE:
no need to get access token.
function get_companies: just run
function get_users_robots: input GUID variable and run
function get_company_robots: input company name and run
function get_company_users: input company name and run
"""


from utils import SpoccClient

spocc_client = SpoccClient("get_ia30_details")

keys = ["companies", "users_robots", "company_robots", "company_users"]

GUID = "3b0bdb9e-67e4-4eca-a4e2-afd85751dcf5"
COMPANY = "JP00219994"


d = ['02a9697e-0cb4-48a8-aa3d-18a2028c8554', '063f5525-e255-4d37-ada2-07744dc9f378', '0680ea09-5001-4031-b0a0-628e5f107a8f', '0e2a5787-2861-4739-af00-57b7bfd7df4e', '10d890d0-dd93-4142-8448-ba9aa011db94', '1379e793-095f-4b40-b92f-27f189e476c1', '23a2abf2-35e8-4266-8d25-881458582620', '2a76a2dc-f623-4cac-9a28-82a779b3f3d8', '2f840600-7b7f-4f0a-9e9e-a5b105a18d97', '2f881d59-ea20-4bd0-911e-8ea22299195f', '40de2ba4-b638-4836-a995-63c06c056ccd', '40f80de8-995f-4540-91de-f98a08207ed4', '41fdb0c0-1b20-46aa-9908-eaa9c1366754', '46c8210e-e245-46fb-b2ae-31d95faf8e6b', '47c33bcc-74bb-4c03-8c44-c1ff858574d9', '4ea7fd67-3394-48a1-b05d-fb5ba7c6d2fb', '5335209f-94f4-408b-88e1-4d0e744fe3c2', '5563a7bf-cd63-4c1b-ade7-9520ddd596b1', '58cf61db-200c-48fd-9f8c-5f65048016bd', '5aa19bf7-a6a1-4107-9234-43871d93984b', '5b10955f-447e-46b2-a5d0-86c01f3e9f34', '5b9c2bbd-434c-4ef6-9332-5e41336f3a89', '5c7f644b-32a4-4563-acb2-21f4ac5de328', '613c1502-3f6c-4d96-b3f4-bda23763f578', '63314f2a-1f5b-4689-82b0-68e97a93c05c', '6a290797-eaaa-410b-8872-65264d6a9b51', '6d43df3e-3286-4cce-9661-6496875a619d', '6d552c35-359b-4393-9107-c16686749248', '9043e28e-4e93-446e-b505-7f02ee9f9ef9', '963c8c4a-e093-4145-9037-7c5dde5a87df', '99f42c19-d66e-4d8e-be71-2cf353db9cdf', '9b1d70e8-7fb4-4b74-8c4d-39d3f3580c0b', '9ce10462-30ad-4731-87d4-658f7e606440', 'a303e02e-efd2-4b5d-b99c-44b05973d7e4', 'a31f01a7-b037-4101-8c7f-dfa95edc266f', 'a3fb4912-5acc-4833-b955-7faf09388ea7', 'a9ac400f-f7f4-4174-a4a7-759f0c05fad4', 'aa5f9923-d5b2-4bc9-97b7-07b8f0ee8caa', 'ab8b2982-2ab9-4ce7-bcb0-c431fbb7506a', 'b0453d13-d85b-49e1-8fe5-1fe248434b7e', 'b459a03f-0353-44f1-bad2-cf6abfb33cb7', 'ba5ecf65-b985-44d0-90ba-824494f20aba', 'bb7afbca-32a7-4945-91a2-f95c66429adf', 'bba6f571-7ef8-414e-aa95-1ce66c2d320c', 'c529216c-9cb6-4626-8347-acffb58857cc', 'c7999a5a-d25f-4ca0-899b-a48dbc1cbdfd', 'c7fb11eb-a001-482f-bf0b-38bd97839378', 'cca062dd-93e7-44a0-adca-7b77350c8309', 'cd96232b-811f-4c02-b1a6-cf9893b4adbd', 'cd9721ea-7df4-439b-af77-f5b35a42bd51', 'ce6d8ed9-a243-4284-a256-efaa1cb3a9a8', 'd23ef36e-254f-44e2-afab-403e4c9d5111', 'd38ad5ab-c8cb-45cf-839a-f687b5ce20f6', 'd5c3f58f-93cb-4d70-b62c-d62284d6173f', 'ddab59e1-3eb6-4867-97b8-fb4ebf5498e6', 'e0eaf84a-b347-43f8-8b36-31990abdcab0', 'e797757f-90f2-49a6-952d-44dce6a250ad', 'eb55f532-a7bc-47f3-bb88-fde118397a7d', 'eb5d4b0c-2ab5-43e1-b099-7be695a75fa2', 'ef446769-c266-4671-b848-df966c01a8dc', 'f6ed62c8-b543-449f-9faf-b2ff8cc88a95', 'f9d3c7f6-071a-4c1c-80fc-d842f0350d22', 'fda655be-09c5-4fc9-be00-6dbfaac38695']

# {'companyKey': 'JP00219994', 'companyName': '進和テック株式会社'}


def get_companies():  # validated
    res: dict = spocc_client.get_info("companies", path="")
    print(res)
    return res


def get_users_robots(r):  # validated
    res: dict = spocc_client.get_info("users_robots", path=r)
    print(res)
    return res


def get_company_robots(c):
    res: dict = spocc_client.get_info("company_robots", path=c)
    print(res)
    return res


def company_users():
    res: dict = spocc_client.get_info("company_users", path=COMPANY)
    print(res)


def main():
    companies = get_users_robots(GUID)
    # for company in companies["companies"]:
    #     if "進和テック" in company["companyName"]:
    #         print(company)
    #         quit()


if __name__ == '__main__':
    main()
