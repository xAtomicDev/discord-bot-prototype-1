from typing import Dict

SEPARATOR = ":"


class NamespaceID:
    def __init__(self, namespace: str, action: str, **params):
        self.namespace = namespace
        self.action = action
        self.params = params

    def build(self) -> str:
        parts = [self.namespace, self.action]

        for key, value in self.params.items():
            parts.append(f"{key}={value}")

        return SEPARATOR.join(parts)

    @staticmethod
    def parse(custom_id: str) -> Dict:
        parts = custom_id.split(SEPARATOR)

        namespace = parts[0]
        action = parts[1]

        params = {}
        for part in parts[2:]:
            if "=" in part:
                k, v = part.split("=", 1)
                params[k] = v

        return {
            "namespace": namespace,
            "action": action,
            "params": params
        }