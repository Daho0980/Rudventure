from .clientSet import FakeClient


client           = FakeClient()
serverConnection = True

history:dict = {"chat": [], "max": 200}
inputText    = []

c = {
    # Normal
    "B" : 0, "M" : 0, "G" : 0, "O" : 0,
    "N" : 0, "P" : 0, "T" : 0, "S" : 0,

    # Bright
    "G1" : 0, "R" : 0, "L" : 0, "Y" : 0,
    "B1" : 0, "F" : 0, "A" : 0, "W" : 0,

    # Hidden Character Color
    "CR" : 0, "CU" : 0,

    # End
    "E" : 0
}

prefix:str = '/'

# region authority settings
authority:dict = {
    "NTS" : {
        0 : "admin",
        1 : "gm",
        2 : "pm",
        3 : "owner",
        4 : "guest"
    },

    "STN" : {
        "admin" : 0,
        "gm"    : 1,
        "pm"    : 2,
        "owner" : 3,
        "guest" : 4
    }
}

currentUserAuthority:set[int] = set([4])

commands:dict = {
    "total" : {
        "say"           : "텍스트를 전송합니다.",
        "help"          : "명령어의 설명을 봅니다.",
        "rule"          : "시스템의 규칙을 확인하거나 변경합니다.",
        "clear"         : "시스템의 히스토리를 모두 비웁니다.",
        "crash"         : "시스템을 충돌시킵니다.",
        "status"        : "플레이어의 상태를 확인하거나 변경합니다.",
        "history"       : "로그 히스토리를 관리합니다.",
        "authorization" : "시스템 유저의 권한을 추가 또는 제거합니다.",
        "auth"          : "authorization과 동일합니다."
    },

    "authorities" : {
        "say" : {
            0 : [4],
            1 : [4]
        },

        "help" : {
            0 : [4],
            1 : [4],
            2 : [4]
        },

        "rule" : {
            0 : [4, 3],
            1 : [4, 3],
            2 : [4, 3],
            3 : [4, 3, 2]
        },

        "clear" : {
            0 : [4]
        },

        "crash" : {
            0 : [4]
        },

        "status" : {
            0 : [4, 3, 1],
            1 : [4, 3, 1]
        },

        "history" : {
            0 : [4, 3],
            1 : [4, 3, 2]
        },

        "authorization" : {
            0 : [4],
            1 : [4],
            2 : [4],
            3 : [4]
        }
    },

    "explanations" : {
        "say" : [
            "/say [text~]",
            "/say -t text=\"[text~]\"(; colorKey=[colorKey])"
        ],

        "help" : [
            "/help",
            "/help [locals || globals]",
            "/help [command]"
        ],

        "rule" : [
            "/rule",
            "/rule [scope]",
            "/rule [scope] [rule]",
            "/rule [scope] [rule] [allowance]"
        ],

        "clear" : [
            "/clear"
        ],

        "crash" : [
            "/crash"
        ],

        "status" : [
            "/status get [status]",
            "/status set [status] [int value]"
        ],

        "history" : [
            "/history size",
            "/history resize [limit]"
        ],

        "authorization" : [
            "authorization current",
            "authorization list",
            "authorization add [authority]",
            "authorization remove [authority]"
        ],
        "auth" : [
            "auth current",
            "auth list",
            "auth add [authority]",
            "auth remove [authority]"
        ],
    },

    "locals" : [
        "say", "rule", "clear", "crash", "history",
        "authorization", "auth"
    ],

    "globals" : ["status"]
}