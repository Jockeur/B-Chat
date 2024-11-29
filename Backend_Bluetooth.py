import bluetooth

# Cette fonction sert à rechercher tout les Appareils Bluetooth Environnant

nearby_devices=bluetooth.discover_devices(duration=15, lookup_names=True, flush_cache=True, lookup_class=True)

