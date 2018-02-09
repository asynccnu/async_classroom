# async_classroom

### 部署应用

服务器，添加环境变量到 **classroom.env** ：

```
    MONGODB_HOST=<host>
    MONGODB_PORT=<port>
```

服务器，命令:

```
    docker-compose -f docker-compose.test.yml build
    docker-compose -f docker-compose.test.yml up &
```


