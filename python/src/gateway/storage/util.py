import pika, json


def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as err:
        return "internal server error", 500
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }
    
    try:
        channel.basic.publish(
            exchange="",
            routhing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTANT_DELIVERY_MODE 
            ),
        )
    except:
        fs.delete(fid)
        return "internal server error", 500
    
    
    