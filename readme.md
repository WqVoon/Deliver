# **API们**

## **说明**

- API 根路径：\<BASEPATH\>:\<PORT\>/
- 为了方便开发，需要点击微信开发者工具的右上角“详情”处，然后点击“本地设置”，设置调试基础库的版本为2.16.0，并勾选下面的“不校验合法域名...”
- **除登录外所有的 API 都需要提供 uuid，所以文档的参数列表中不再添加相关内容，POST 相关的方法提供参数均使用 json**

## **用户登录**

效果：

- 用于登录用户并获取 uuid

概述：

- API路径：\<BASEPATH\>:\<PORT\>/auth/login
- http方法：POST

- 参数：code，appid，secret，raw_data，signature

- 返回值：

  成功返回状态码 200 以及 JSON 格式的内容：{

    "uuid": \<用户认证id\>,

    "tele": \<当前用户的号码\>,

    "addr": [

      {"key": 地址的主键, "location": 地址的字符串表示}
    
      ...

    ]

  }

  失败返回 Err 字符串，状态码 403

说明：

1. 小程序前端需调用 wx.getUserProfile 方法获取用户的基本信息，其中包括 userInfo，rawData，signature 等，userInfo 中可以获取用户的微信昵称、性别、头像路径等信息，用来渲染到前端的视图上
2. 调用 wx.login 从微信服务器获取临时登录凭证 code
3. appid 可在右上角“详情”的“基本信息”中找到，secret 可在“微信公众平台”获得
4. 将上述信息收集完毕后，调用 wx.request 按照前面概述的内容发起请求，若成功则获得用户唯一标识 uuid，将这个值保存到本地，以后发请求时带着它
5. appid 和 secret 本来并不应该提供，后面部署到生产环境时要取消这两个参数
6. 因为一些不明原因，有时后端计算用户的签名时会出现不一致的情况导致登录失败，目前可以二次登录来解决，后面尝试找到原因



## **用户登出**

效果：

- 将用户的 uuid 标记为无效

概述：

- API路径：\<BASEPATH\>:\<PORT\>/auth/logout
- http方法：POST

- 参数：uuid
- 返回值：成功返回“Logout OK”，没处理失败的情况



## **用户登录测试**

效果：

- 用于测试用户是否登录成功

概述：

- API路径：\<BASEPATH\>:\<PORT\>/test/loginTest
- http方法：GET 或 POST
- 参数：uuid
- 返回值：成功返回“Hello \<用户信息\>”，失败返回 405 状态码

说明：

1. 在用户成功登录后，会拿到用户唯一标识 uuid，此后使用需要登录后才能访问的接口时需要带上这个参数，否则不提供服务
2. 本接口用于测试该 uuid 的有效性，若能调用成功，则其他需要登录的接口也能正常使用



## **更新电话号码**

概述：

- API路径：\<BASEPATH\>:\<PORT\>/me/tele/update
- http方法：POST

- 参数：tele，表示新的电话号码
- 返回值：方法有调用问题返回 403 状态码和提示信息，否则返回 OK 字符串



## **添加新的常用地址**

概述：

- API路径：\<BASEPATH\>:\<PORT\>/me/addr/add
- http方法：POST

- 参数：addrs，一个字符串列表，其中的每一个字符串代表一个地址

- 返回值：

  方法有调用问题返回 403 状态码和提示信息，否则返回 JSON 格式的内容（表示新添加的地址）：{

    "addrs": [

      {"key": \<数据库主键\>, "location": \<地址文本\>},
    
      ...

    ]

  }



## **删除常用地址**

概述：

- API路径：\<BASEPATH\>:\<PORT\>/me/addr/delete
- http方法：POST

- 参数：addrs，一个列表，其中的每一项代表待删除记录的主键

- 返回值：方法有调用问题返回 403 状态码和提示信息，否则返回 OK 字符串



## **修改常用地址**

概述：

- API路径：\<BASEPATH\>:\<PORT\>/me/addr/update
- http方法：POST
- 参数：addrs，一个列表，其中的每一项形如 {"key": \<数据库主键\>, "location": \<新的地址文本\>}

- 返回值：方法有调用问题返回 403 状态码和提示信息，否则返回 OK 字符串



## **添加订单**

概述：

- API路径：\<BASEPATH\>:\<PORT\>/pending/add

- http方法：POST

- 参数：{

    "amount": \<价格\>,

    "comments": \<备注\>,

    "stuff_number": \<物品数量\>

    "stuff_weight": \<物品重量\>

    "stuff_address": \<取件地址\>

    "receive_address": \<收件地址\>

  }

- 返回值：方法有调用问题返回 403 状态码和提示信息，否则返回 OK 字符串



## **查询所有待接取的订单**

概述：

- API路径：\<BASEPATH\>:\<PORT\>/pending/query/all/\<页面\>

- http 方法：GET

- 参数：无

- 返回值：没有对应的页返回 404，否则返回 JSON，其 items 属性为一个列表，列表中的每一项为：{

    id: \<订单主键\>

    stuff_number: \<物品数量\>

    stuff_weight: \<物品重量\>

    stuff_address: \<取件地址\>

    receive_address: \<收件地址\>

    amount: \<预付金额\>

    timestamp: \<下单时间\>

    buyer_tele: \<下单人电话\>

    receiver_tele: \<接单人电话\>

    comments: \<备注\>

  }



## **查询我下的所有还未被接取的订单**

概述：

- API路径：\<BASEPATH\>:\<PORT\>/pending/query/i-add/\<页面\>

- 其余同“查询所有待接取的订单“接口



## **接取订单**

概述：

- API路径：\<BASEPATH\>:\<PORT\>/pending/fetch
- http方法：POST
- 参数：key，表示要接取的订单的主键
- 返回值：方法有调用问题返回 403 状态码和提示信息，否则返回 OK 字符串



## **查询我下的所有已经被接取但未完成的订单**

概述：

- API路径：\<BASEPATH\>:\<PORT\>/active/query/i-add/\<页面\>

- 其余同“查询所有待接取的订单“接口



## **查询我接取的所有未完成的订单**

概述：

- API路径：\<BASEPATH\>:\<PORT\>/active/query/i-fetch/\<页面\>

- 其余同“查询所有待接取的订单“接口



## **完成指定订单**

概述：

- API路径：\<BASEPATH\>:\<PORT\>/active/finish
- http方法：POST
- 参数：key，表示要完成的订单的主键

- 返回值：方法有调用问题返回 403 状态码和提示信息，否则返回 OK 字符串



## **查询我下的所有已完成的订单**

概述：

- API路径：\<BASEPATH\>:\<PORT\>/finish/query/i-add/\<页面\>

- 其余同“查询所有待接取的订单“接口



## **查询我接取的所有已完成的订单**

概述：

- API路径：\<BASEPATH\>:\<PORT\>/finish/query/i-fetch/\<页面\>

- 其余同“查询所有待接取的订单“接口