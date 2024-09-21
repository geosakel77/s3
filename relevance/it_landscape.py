from mitreattack.stix20 import MitreAttackData


def get_assets_db():
    mitre_attack_data = MitreAttackData("../dataset/cti/enterprise-attack/enterprise-attack.json")

    assets = mitre_attack_data.get_assets()
    print(assets)
    print(f"Retrieved {len(assets)} ICS assets.")


if __name__ == "__main__":
    get_assets_db()
