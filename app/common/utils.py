def update_model(model, data):
    for key, value in data.items():
        setattr(model, key, value)
    return model