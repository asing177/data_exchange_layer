def execute_mar_search_api(client, payload_dict):
    """
    Executes a query against the MAR search api

    :param client: The DXL client
    :param payload_dict: The payload
    :return: A dictionary containing the results of the query
    """
    # Create the request message
    req = Request(CREATE_SEARCH_TOPIC)
    # Set the payload
    req.payload = json.dumps(payload_dict).encode(encoding="UTF-8")

    # Display the request that is going to be sent
    print("Request:\n" + json.dumps(payload_dict, sort_keys=True, indent=4, separators=(',', ': ')))

    # Send the request and wait for a response (synchronous)
    res = client.sync_request(req, timeout=30)

    # Return a dictionary corresponding to the response payload
    if res.message_type != Message.MESSAGE_TYPE_ERROR:
        resp_dict = json.loads(res.payload.decode(encoding="UTF-8"))
        # Display the response
        print("Response:\n" + json.dumps(resp_dict, sort_keys=True,
                                         indent=4, separators=(',', ': ')))
        if "code" in resp_dict:
            code = resp_dict['code']
            if code < 200 or code >= 300:
                if "body" in resp_dict and "applicationErrorList" in resp_dict["body"]:
                    error = resp_dict["body"]["applicationErrorList"][0]
                    raise Exception(error["message"] + ": " + str(error["code"]))
                elif "body" in resp_dict:
                    raise Exception(resp_dict["body"] + ": " + str(code))
                else:
                    raise Exception("Error: Received failure response code: " + str(code))
        else:
            raise Exception("Error: unable to find response code")
        return resp_dict
    else:
        raise Exception("Error: " + res.error_message + " (" + str(res.error_code) + ")")