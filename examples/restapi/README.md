

Please add your credentials to the `env_example` file and rename it to `.env`. Then, run the following command:

```shell
docker-compose up
```

or


```shell
docker build --build-arg HOST_NAME=your_host_name --build-arg SENDER_COMPID=your_sender_compid --build-arg PASSWORD=your_password -t your_image .
```

```shell
docker run -e "HOST_NAME=your_host_name" -e "SENDER_COMPID=your_sender_compid" -e "PASSWORD=your_password" your_image
```