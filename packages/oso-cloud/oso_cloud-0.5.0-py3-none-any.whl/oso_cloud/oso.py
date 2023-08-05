import json
from typing import cast, Dict, Optional

import requests

# takes string or class instance
def extract_typed_id(obj) -> Dict[str, str]:  # { "type": "type", "id": "id" }
    if type(obj) is str:
        return {"type": "String", "id": obj}
    if not hasattr(obj, "__dict__"):
        raise TypeError(
            f"Expected a string or an instance of a class but received: {obj}"
        )
    if not hasattr(obj, "id"):
        raise TypeError(f"Expected {obj} to have an 'id' attribute")
    return {"type": obj.__class__.__name__, "id": str(obj.id)}


# takes string or
def extract_arg_query(
    obj,
) -> Dict[str, Optional[str]]:  # { "type": "type" | None, "id": "id" | None }
    if obj is None:
        return {"type": None, "id": None}
    if isinstance(obj, type):
        return {"type": obj.__name__, "id": None}
    try:
        return cast(Dict[str, Optional[str]], extract_typed_id(obj))
    except TypeError:
        raise TypeError(
            f"Expected None, a string, a class, or an instance of a class, but received: {obj}"
        )


class Oso:
    def __init__(self, url="https://cloud.osohq.com", api_key=None):
        self.url = url
        self.api_base = "api"
        if api_key:
            self.token = api_key
        else:
            raise ValueError("Must set an api_key")

    def _handle_result(self, result):
        if not result.ok:
            code, text = result.status_code, result.text
            msg = f"Got unexpected error from Oso Service: {code}\n{text}"
            raise Exception(msg)
        try:
            return result.json()
        except json.decoder.JSONDecodeError:
            return result.text

    def _default_headers(self):
        return {
            "Authorization": f"Basic {self.token}",
            "User-Agent": "Oso Cloud (python)",
        }

    def _do_post(self, url, json):
        return requests.post(url, json=json, headers=self._default_headers())

    def _do_get(self, url, params):
        return requests.get(url, params=params, headers=self._default_headers())

    def _do_delete(self, url, json):
        return requests.delete(url, json=json, headers=self._default_headers())

    def authorize(self, actor, action, resource):
        actor_typed_id = extract_typed_id(actor)
        resource_typed_id = extract_typed_id(resource)
        result = self._do_post(
            f"{self.url}/{self.api_base}/authorize",
            json={
                "actor_type": actor_typed_id["type"],
                "actor_id": actor_typed_id["id"],
                "action": action,
                "resource_type": resource_typed_id["type"],
                "resource_id": resource_typed_id["id"],
            },
        )
        allowed = self._handle_result(result)["allowed"]
        return allowed

    def authorize_resources(self, actor, action, resources):
        def key(e: Dict) -> str:  # { "type": "type", "id": "id" }
            return f"{e['type']}:{e['id']}"

        if not resources or len(resources) == 0:
            return []

        resources_extracted = [extract_typed_id(r) for r in resources]
        actor_typed_id = extract_typed_id(actor)
        result = self._do_post(
            f"{self.url}/{self.api_base}/authorize_resources",
            json={
                "actor_type": actor_typed_id["type"],
                "actor_id": actor_typed_id["id"],
                "action": action,
                "resources": resources_extracted,
            },
        )
        results = self._handle_result(result)["results"]
        if len(results) == 0:
            return []

        results_lookup = dict()
        for r in results:
            k = key(r)
            if not results_lookup.get(k, None):
                results_lookup[k] = True

        return list(
            filter(
                lambda r: results_lookup.get(key(extract_typed_id(r)), None),
                resources,
            )
        )

    def list(self, actor, action, resource_type):
        actor_typed_id = extract_typed_id(actor)
        result = self._do_post(
            f"{self.url}/{self.api_base}/list",
            json={
                "actor_type": actor_typed_id["type"],
                "actor_id": actor_typed_id["id"],
                "action": action,
                "resource_type": resource_type,
            },
        )
        results = self._handle_result(result)["results"]
        return results
    
    def actions(self, actor, resource):
        actor_typed_id = extract_typed_id(actor)
        resource_typed_id = extract_typed_id(resource)
        result = self._do_post(
            f"{self.url}/{self.api_base}/actions",
            json={
                "actor_type": actor_typed_id["type"],
                "actor_id": actor_typed_id["id"],
                "resource_type": resource_typed_id["type"],
                "resource_id": resource_typed_id["id"],
            },
        )
        results = self._handle_result(result)["results"]
        return results

    def tell(self, predicate, *args):
        result = self._do_post(
            f"{self.url}/{self.api_base}/facts",
            json={"predicate": predicate, "args": list(map(extract_typed_id, args))},
        )
        return self._handle_result(result)

    def bulk_tell(self, facts):
        args = [
            {"predicate": predicate, "args": list(map(extract_typed_id, args))}
            for [predicate, *args] in facts
        ]
        result = self._do_post(
            f"{self.url}/{self.api_base}/bulk_load",
            json=args,
        )
        return self._handle_result(result)

    def delete(self, predicate, *args):
        result = self._do_delete(
            f"{self.url}/{self.api_base}/facts",
            json={"predicate": predicate, "args": list(map(extract_typed_id, args))},
        )
        return self._handle_result(result)

    def bulk_delete(self, facts):
        args = [
            {"predicate": predicate, "args": list(map(extract_typed_id, args))}
            for [predicate, *args] in facts
        ]
        result = self._do_post(
            f"{self.url}/{self.api_base}/bulk_delete",
            json=args,
        )
        return self._handle_result(result)

    def get(self, predicate=None, *args):
        params = {}
        if predicate:
            params["predicate"] = predicate
        for i, arg in enumerate(args):
            arg_query = extract_arg_query(arg)
            params[f"args.{i}.type"] = arg_query["type"]
            params[f"args.{i}.id"] = arg_query["id"]
        result = self._do_get(f"{self.url}/{self.api_base}/facts", params=params)
        return self._handle_result(result)

    def policy(self, policy):
        result = self._do_post(
            f"{self.url}/{self.api_base}/policy", json={"src": policy}
        )
        return self._handle_result(result)
