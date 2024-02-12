import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor


def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    # empy temp file 
    tf = tempfile.NamedTemporaryFile()
    # video contents
    out = fs_videos.get(ObjectId(message["video_fid"]))
    # add video contents to empty file
    tf.write(out.read())
    # convert temp video file into audio
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()
    
    # write the audio to its own file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path) # this created the temp file
    
    # save the file to mongo
    f = open(tf_path, "rb") 
    fid = fs_mp3s.put(data) # we are storing the temp file in gridfs
    f.close()
    os.remove(tf_path) # deleting this temp file 
    
    # placing the message on the queue
    message["mp3_fid"] = str(fid)
    
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err: # if we cant place the message on the queue, we want to delete mp3 from mongo
        fs_mp3s.delete(fid)
        return "failed to publish message"
    
    
    