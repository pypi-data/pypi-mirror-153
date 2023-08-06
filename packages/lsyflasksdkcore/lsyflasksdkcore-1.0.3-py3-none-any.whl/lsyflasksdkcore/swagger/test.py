"""
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#requestBodyObject
Gist detail view.
---
post:
  tags:
    - pet
  summary: "test"
  requestBody:
    content:
      application/json:
        schema:
          type: object
          required:
            - timestamp
          properties:
            timestamp:
              type: integer
              format: int64
              description: 时间戳
            body: Baidu1Schema
  responses:
    200:
      content:
        application/json:
          schema:
            type: object
            properties:
              code:
                type: integer
                description: http code
              error:
                type: boolean
                description: is error
              message:
                type: string
                description: 返回消息
              total:
                type: integer
                description: 总页数
              data:
                type: array
                items:
                  GistSchema
                description: data description
"""


# @app.route("/gists1", methods=['GET', 'POST'])
def gist_detail1():
    """gist_detail1 views
    ---
    post:
      tags:
        - pet
      summary: "fdsfdsfdsfdsfdsfdsfd"
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required:
                - timestamp
              properties:
                timestamp:
                  type: integer
                  format: int64
                  required: true
                  description: 时间戳
                body: Baidu1Schema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                    description: http code
                  error:
                    type: boolean
                    description: 是否错误
                  message:
                    type: string
                    description: 返回消息
                  total:
                    type: integer
                    description: 总页数
                  data:
                    type: array
                    items:
                      GistSchema
                    description: 我是GistSchema
    """
    return "details about gist {}".format("fdsfdsfdsfdsf")
