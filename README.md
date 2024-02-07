                                Video to MP3 Conversion Workflow
                                        Overview

    This document outlines the workflow for converting uploaded videos to MP3 format
    and serving them to clients.
        
                                            Workflow Steps

    User Uploads Video:
        When a user uploads a video, the request is sent to our gateway.

    Request Handling:
        Our gateway stores the request in MongoDB.
        A message is placed on our queue (RabbitMQ), signaling downstream services about the
        video to be processed.

    Conversion Service:
        The video-to-MP3 converter service consumes messages from the queue.
        It retrieves the ID from the message, pulls the video from MongoDB, and converts it 
        to MP3 format.
        The resulting MP3 is stored in MongoDB.
        A new message is placed in RabbitMQ for the notification service.

    Notification Service:
        The notification service consumes messages from the queue.
        It sends an email to the client, notifying them that the MP3 conversion is complete
        and ready for download.

    Client Download:
        The client, using a unique ID acquired from the notification along with JWT
        authentication, requests the MP3 download via the API gateway.

    API Gateway:
        The API gateway retrieves the MP3 from MongoDB.
        It serves the MP3 file to the client for download.

                                            
                                            Usage

    Users can upload videos for conversion to MP3 format through the provided interface.
    Upon successful conversion, users receive an email notification with a link to download
    the MP3 file. Clients can download the converted MP3 file using the provided unique 
    ID and JWT authentication via the API gateway.
