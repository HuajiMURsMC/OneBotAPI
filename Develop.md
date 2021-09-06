# 开发文档

## 调用 OneBot API

由于实现了 `__getattr__` 魔术方法，所以你可以直接在 `api` 对象上直接调用 OneBot API

例如：

```python
api.send_private_msg(user_id=10001000, message="你好")
friends = api.get_friend_list()
```

当然你也可以直接使用 `call_api` 函数来调用，如：

```python
api.call_api('set_group_whole_ban', group_id=10010)
```

## 接收 OneBot 事件

所有的事件都会以 `onebot_api.qq.事件类型` 的样子进行分发

事件类型可以为：

- `message`：消息事件
- `notice`：通知事件
- `request`：请求事件
- `meta_event`：元事件

每个事件都只包含了两个参数：

`ServerInterface` 和 `OneBot 事件的 JSON`

