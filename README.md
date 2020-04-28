# Chat Room

[TOC]



## 前言

API写的大概可以了，除了文件上传和websocket没测试外。。。在这个API中，所有数据的返回格式都是这样子的

```bash
{
	"status": 200,
	"message": "succeed",
	"data": {}
}
```

其中status为状态码，若状态码不为200的话，则说明资源请求失败，比如没有权限什么的。当然状态码我也会在响应头里面设置。然后message为请求状态信息，若状态码为200，则message固定为“succeed", 若状态码不为200，则message为对应的错误消息。然后data为一个字典，里面包含了所请求的数据。

然后在这个接口，我对权限之类的都判定好了，比如用户未加入该房间没权限请求房间消息，也没权限请求房间中的消息消息，不是房主也无权限更改房间信息什么的。。这些我都会判断出来，若请求失败则会返回对应的状态码及消息。当然除了权限判断之外还会判断一些七七八八的，总之状态码若不为200则为请求失败。然后一些七七八八的请求失败对应的message是什么你可以问我。然后又比如加入房间的秘钥不正确的话会这样子返回

```bash
{
	"status": 401,
	"message": "invalid access key"
}
```

大概就是这样子吧，冲鸭！！！



## 用户接口

用户在第一次向该API发送请求时会自动创建一个用户，故不存在创建用户接口。

### 获取用户

#### 请求方式

请求方法：GET

请求URL： http://chatroom.mr-lin.site/api/v1/user

请求参数：无

#### 返回示例

```bash
{
    "data": {
        "avatar": "http://chatroom.mr-lin.site/avatars/user/25",  #头像链接
        "create_at": "2020-04-25 11:45:36.129983",  #创建时间
        "id": 25,  
        "kind": "User",  #数据类型
        "messages": [],  #消息信息列表， 具体内容详见消息接口的
        "rooms": [],  #房间信息列表， 具体内容详见房间接口
        "self": "http://chatroom.mr-lin.site/api/v1/user/",  #当前资源请求链接
        "update_at": "2020-04-25 11:45:36.129983",  #更新时间
        "username": "customer25",   #用户名
        "phone": "2333",
        "email": "2333@qq.com",
        "country": "China",
        "area": "fujian"
    },
    "message": "succeed",
    "status": 200
}
```



### 修改用户信息

#### 请求方式

请求方法：PUT

请求URL： http://chatroom.mr-lin.site/api/v1/user

请求参数：

| 参数名   | 必须 | 类型   | 说明           |
| -------- | ---- | ------ | -------------- |
| username | 否   | string | 要更改的用户名 |
| phone    | 否   | string |                |
| email    | 否   | string |                |
| country  | 否   | string |                |
| area     | 否   | string |                |

用户名不能重复，若重复不会返回用户数据，响应状态码不为200.

#### 返回示例

```bash
# 返回用户信息，与获取用户相同
{
    "data": {
        "avatar": "http://chatroom.mr-lin.site/avatars/user/25",
        "create_at": "2020-04-25 11:45:36.129983",
        "id": 25,
        "kind": "User",
        "messages": [],
        "rooms": [],
        "self": "http://chatroom.mr-lin.site/api/v1/user/",
        "update_at": "2020-04-25 11:45:36.129983",
        "username": "3927"
    },
    "message": "succeed",
    "status": 200
}
```



### 删除用户

#### 请求方式

请求方法：DELETE

请求URL： http://chatroom.mr-lin.site/api/v1/user

请求参数：无

#### 返回示例

```bash
# 返回用户信息，与获取用户相同
{
    "data": {
        "avatar": "http://chatroom.mr-lin.site/avatars/user/25",
        "create_at": "2020-04-25 11:45:36.129983",
        "id": 25,
        "kind": "User",
        "messages": [],
        "rooms": [],
        "self": "http://chatroom.mr-lin.site/api/v1/user/",
        "update_at": "2020-04-25 11:45:36.129983",
        "username": "3927"
    },
    "message": "succeed",
    "status": 200
}
```

在删除发送delete请求后请务必清除cookies中的token数据，否则用户在该浏览器无法再次使用接口



### 加入房间与退出房间

#### 说明

该加入房间与退出房间为对用户所加入的房间信息的修改，而非单纯的加入/离开聊天时的加入/离开房间

。。。。。。

就是说，用户不是可以加入多个房间嘛，所以用户加入的房间的信息应该保留，这个接口是对用户的房间列表进行操作

#### 请求方式

请求方法：PUT

请求URL： http://chatroom.mr-lin.site/api/v1/user

请求参数：

| 参数名  | 必须 | 类型   | 说明                   |
| ------- | ---- | ------ | ---------------------- |
| room_id | 否   | int    | 要更改的用户名         |
| action  | 是   | string | 应为 'join' 或 'leave' |
| key     | 否   | string | 若加入房间则为必须     |
| name    | 否   | string |                        |

action为join时，key与name为必须。action为leave时，room_id为必须。

#### 返回示例

```bash
# 返回房间信息
{
  "data": {
    "avatar": "http://127.0.0.1/avatars/room/1",
    "create_at": "Sun, 26 Apr 2020 01:37:30 GMT",
    "id": 1,
    "introduce": "the master is so lazy!",
    "kind": "Room",
    "messages": [],
    "name": "room1",
    "self": "http://127.0.0.1/api/v1/room/1",
    "updated_at": "Sun, 26 Apr 2020 01:37:30 GMT",
    "users": [
      {
        "avatar": "http://127.0.0.1/avatars/user/1",
        "create_at": "2020-04-26 01:35:47",
        "id": 1,
        "kind": "User",
        "self": "http://127.0.0.1/api/v1/user/",
        "update_at": "2020-04-26 01:35:47",
        "username": "customer1"
      },
      {
        "avatar": "http://127.0.0.1/avatars/user/2",
        "create_at": "2020-04-26 01:42:24",
        "id": 2,
        "kind": "User",
        "self": "http://127.0.0.1/api/v1/user/",
        "update_at": "2020-04-26 01:42:24",
        "username": "customer2"
      }
    ]
  },
  "message": "succeed",
  "status": 200
}
```



### 获取某一房间全部用户信息

其实这个接口没什么用啦。。因为请求房间信息的时候用户信息也会发给你。

该加入房间与退出房间为对用户所加入的房间信息的修改，而非单纯的加入/离开聊天时的加入/离开房间

。。。。。。

就是说，用户不是可以加入多个房间嘛，所以用户加入的房间的信息应该保留，这个接口是对用户的房间列表进行操作

#### 请求方式

请求方法：GET

请求URL： http://chatroom.mr-lin.site/api/v1/users?room=room_id

请求参数：无

#### 返回示例

```bash
# 返回用户列表信息，与获取用户相同，明显可见rooms里面多了个房间信息
{
    "data": {
        "count": 1,  # 用户数据个数(即users中的用户个数)
        "kind": "UserList",  # 资源类型
        "self": "http://chatroom.mr-lin.site/api/v1/users/?room=1",  # 该资源请求链接
        "users": [  # 用户信息
            {
                "avatar": "http://chatroom.mr-lin.site/avatars/user/25",
                "create_at": "2020-04-25 11:45:36.129983",
                "id": 25,
                "kind": "User",
                "self": "http://chatroom.mr-lin.site/api/v1/user/",
                "update_at": "2020-04-25 11:45:36.129983",
                "username": "3927"
            }
        ]
    },
    "message": "succeed",
    "status": 200
}
```

## 房间接口

### 获取房间

#### 请求方式

请求方法：GET

请求URL： http://chatroom.mr-lin.site/api/v1/room/rid_or_name

​		example:http://chatroom.mr-lin.site/api/v1/room/1, http://chatroom.mr-lin.site/api/v1/room/test

请求参数：无

#### 返回示例

```bash
{
    "data": {
        "avatar": "http://chatroom.mr-lin.site/avatars/room/1",  #房间头像URL
        "create_at": "Sat, 25 Apr 2020 12:21:59 GMT",  #创建日期
        "id": 1, 
        "introduce": "2333",  # 房间简介
        "kind": "Room",  #资源类型
        "messages": [],  # 房间消息列表，具体内容详见message接口
        "name": "test4",  # 房间名称
        "master_id": 1,  # 房主ID
        "self": "http://chatroom.mr-lin.site/api/v1/room/1",  # 该资源请求URL
        "updated_at": "Sat, 25 Apr 2020 12:21:59 GMT",  # 更新日期
        "users": [  # 房间用户列表
            {
                "avatar": "http://chatroom.mr-lin.site/avatars/user/25",
                "create_at": "2020-04-25 11:45:36.129983",
                "id": 25,
                "kind": "User",
                "self": "http://chatroom.mr-lin.site/api/v1/user/",
                "update_at": "2020-04-25 11:45:36.129983",
                "username": "3927"
            }
        ]
    },
    "message": "succeed",
    "status": 200
}
```



### 创建房间

#### 请求方式

请求方法：POST

请求URL： http://chatroom.mr-lin.site/api/v1/rooms/

请求参数： 请求参数应该在json数据中，非json中的数据不会接收

| 参数名    | 必须 | 类型   | 说明                 |
| --------- | ---- | ------ | -------------------- |
| name      | 否   | string | 房间名               |
| introduce | 否   | string | 房间简介             |
| key       | 否   | string | 房间秘钥，默认123456 |

#### 返回示例

```bash
# 返回房间信息，与获取房间相同
{
    "data": {
        "avatar": "http://chatroom.mr-lin.site/avatars/room/1",
        "create_at": "Sat, 25 Apr 2020 12:21:59 GMT",
        "id": 1,
        "introduce": "welcome",
        "kind": "Room",
        "messages": [],
        "name": "test5",
        "self": "http://chatroom.mr-lin.site/api/v1/room/1",
        "updated_at": "Sat, 25 Apr 2020 12:21:59 GMT",
        "users": [
            {
                "avatar": "http://chatroom.mr-lin.site/avatars/user/25",
                "create_at": "2020-04-25 11:45:36.129983",
                "id": 25,
                "kind": "User",
                "self": "http://chatroom.mr-lin.site/api/v1/user/",
                "update_at": "2020-04-25 11:45:36.129983",
                "username": "3927"
            }
        ]
    },
    "message": "succeed",
    "status": 200
}
```



### 删除房间

#### 请求方式

请求方法：DELETE

请求URL： http://chatroom.mr-lin.site/api/v1/user

请求参数：无

#### 返回示例

```bash
# 返回房间信息
{
    "data": {
        "avatar": "http://chatroom.mr-lin.site/avatars/room/3",
        "create_at": "Sat, 25 Apr 2020 14:52:46 GMT",
        "id": 3,
        "introduce": "2333",
        "kind": "Room",
        "messages": [],
        "name": "test",
        "self": "http://chatroom.mr-lin.site/api/v1/room/3",
        "updated_at": "Sat, 25 Apr 2020 14:52:46 GMT",
        "users": [
            {
                "avatar": "http://chatroom.mr-lin.site/avatars/user/28",
                "create_at": "2020-04-25 14:52:31.624728",
                "id": 28,
                "kind": "User",
                "self": "http://chatroom.mr-lin.site/api/v1/user/",
                "update_at": "2020-04-25 14:52:31.624728",
                "username": "customer28"
            }
        ]
    },
    "message": "succeed",
    "status": 200
}
```



### 修改房间信息

#### 请求方式

请求方法：PUT

请求URL： http://chatroom.mr-lin.site/api/v1/room/rid_or_name

请求参数： 

| 参数名    | 必须 | 类型   | 说明           |
| --------- | ---- | ------ | -------------- |
| name      | 否   | string | 要更改的房间名 |
| introduce | 否   | string | 更改的介绍     |
| key       | 否   | string | 更改的秘钥     |

#### 返回示例

```bash
# 返回房间信息
{
    "data": {
        "avatar": "http://chatroom.mr-lin.site/avatars/room/3",
        "create_at": "Sat, 25 Apr 2020 14:55:50 GMT",
        "id": 3,
        "introduce": "welcome",
        "kind": "Room",
        "messages": [],
        "name": "test666",
        "self": "http://chatroom.mr-lin.site/api/v1/room/3",
        "updated_at": "Sat, 25 Apr 2020 14:55:50 GMT",
        "users": [
            {
                "avatar": "http://chatroom.mr-lin.site/avatars/user/28",
                "create_at": "2020-04-25 14:52:31.624728",
                "id": 28,
                "kind": "User",
                "self": "http://chatroom.mr-lin.site/api/v1/user/",
                "update_at": "2020-04-25 14:52:31.624728",
                "username": "customer28"
            }
        ]
    },
    "message": "succeed",
    "status": 200
}
```



## 消息接口

### 获取消息
#### 请求方式

请求方法：GET

请求URL： http://127.0.0.1:80/api/v1/message/message_id

请求参数： 无

#### 返回示例

```bash
{
    "data": {
        "author": "customer28",  # 作者用户名
        "content": "test5",  # 消息内容，若消息种类为文件的话，为文件名
        "create_at": "2020-04-25 15:04:50.753855",  # 创建日期
        "id": 1,  
        "kind": "Message", #资源种类
        "room": "test666", #房间
        "self": "http://chatroom.mr-lin.site/api/v1/message/1",  #资源自身URL，若为文件，则为文件获取url
        "type": "text",  # 消息种类(text/file/picture)
        "updated_at": "2020-04-25 15:04:50.753855"
    },
    "message": "succeed",
    "status": 200
}
```



### 创建消息

#### 请求方式

请求方法：POST

请求URL： http://chatroom.mr-lin.site/api/v1/messages/room_id

请求参数： 创建消息时的请求参数不必再json里，可以直接在表单数据中。若上传文件，则需要设置表单属性enctype="multipart/form-data"。

| 参数名  | 必须 | 类型   | 说明                 |
| ------- | ---- | ------ | -------------------- |
| type    | 是   | string | text/file/content    |
| content | 是   | string | 若为文件，则为文件名 |

#### 返回示例

```bash
# 返回消息信息。
{
    "data": {
        "author": "customer28",
        "content": "test5",
        "create_at": "2020-04-25 15:04:50.753855",
        "id": 1,
        "kind": "Message",
        "room": "test666",
        "self": "http://chatroom.mr-lin.site/api/v1/message/1",
        "type": "text",
        "updated_at": "2020-04-25 15:04:50.753855"
    },
    "message": "succeed",
    "status": 200
}
```



### 获取某一房间所有消息

#### 请求方式

请求方法：GET

请求URL： http://chatroom.mr-lin.site/api/v1/messages/room_id

请求参数： 无

#### 返回示例

```bash
# 返回消息列表信息。
{
    "data": {
        "count": 1,  #消息数目
        "kind": "MessageList",  #资源类型
        "messages": [  # 消息列表
            {
                "author": "customer28",
                "content": "test5",
                "create_at": "2020-04-25 15:04:50.753855",
                "id": 1,
                "kind": "Message",
                "room": "test666",
                "self": "http://chatroom.mr-lin.site/api/v1/message/1",
                "type": "text",
                "updated_at": "2020-04-25 15:04:50.753855"
            }
        ],
        "self": "http://chatroom.mr-lin.site/api/v1/messages/3"  #该资源请求URL
    },
    "message": "succeed",
    "status": 200
}
```



### 关于消息搜索

请求URL：http://chatroom.mr-lin.site/api/v1/search?q=keyword&rid=room_id

返回示例

```
 # 返回消息列表
 {
    "data": {
        "count": 1,
        "kind": "MessageList",
        "messages": [
            {
                "author": "customer28",
                "content": "test5",
                "create_at": "2020-04-25 15:04:50.753855",
                "id": 1,
                "kind": "Message",
                "room": "test666",
                "self": "http://chatroom.mr-lin.site/api/v1/message/1",
                "type": "text",
                "updated_at": "2020-04-25 15:04:50.753855"
            }
        ],
        "self": "http://chatroom.mr-lin.site/api/v1/messages/3"
    },
    "message": "succeed",
    "status": 200
}
```



## 关于websocket

这边需要你在用户发送消息，进入房间，退出房间时用websocket向我发送一条消息以实时显示谁加入了房间，谁退出了房间，注意，这个加入与退出房间与向用户的房间列表添加或删除房间不同，只是单纯的用户加入某个房间进行聊天。

### 发送消息

发送事件名称："new message",所需数据：消息id

```html
<!--示例--><button onclick="socket.emit('new message', 1)">new message</button>
```

我收到消息后会用websocket向在房间中的每一个客户端发送一个名为“new message" 的事件，发送的数据为一个字典，字典内容参照消息消息里面”data“键对应的值<a href="#获取消息">快速链接</a>



### 加入房间

发送事件名称："join room",所需数据：房间id及用户名
```html
<!--示例--><button onclick="socket.emit('join room', {'id': '1', 'username': 'lin'})">join room1</button>
```

我收到消息后会用websocket向在房间中的每一个客户端发送一个名为“join room" 的事件，发送的数据为加入房间的用户的用户名。




### 离开房间

发送事件名称："leave room",所需数据：房间id及用户名
```html
<!--示例--><button onclick="socket.emit('leave room', {'id': '1', 'username': 'lin'})">leave room1</button>
```

我收到消息后会用websocket向在房间中的每一个客户端发送一个名为“leave room" 的事件，发送的数据为加入房间的用户的用户名。



## 关于头像请求

虽然在获取房间或者用户信息的时候会告诉你头像的URL啦，但还是把头像URL规则告诉你好了

房间头像：chatroom.mr-lin.site/avatars/room/room_id

用户头像：chatroom.mr-lin.site/avatars/user/user_id

关于修改头像：链接跟获取头像相同，只不过方法为POST，然后在表单里面带上文件就可以了。name属性应该为avatar



## 关于资源请求

文件及图片资源的请求我也像头像一样告诉你好了

文件：chatroom.mr-lin.site/files/message_id

图片：chatroom.mr-lin.site/pictures/message_id