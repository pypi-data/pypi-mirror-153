config_json = {
    "online": {
        "log_level": {
            "console": "ERROR",
            "file": "DEBUG",
            "third_log": True
        },
        "alarm": {
            "secret": "SEC0bb5fc4f03725bdb95b7647f22cffae20883c155354545cbcc9a283badd7b5a6",
            "url": "https://oapi.dingtalk.com/robot/send?access_token=23d1a07564a391d2d9041954bdaa1db0a3c3b231366ac314d6bd289ec0dc9e4f",
            "atMobiles": [],
            "isAtAll": True
        }
    },
    "pre": {
        "log_level": {
            "console": "ERROR",
            "file": "DEBUG",
            "third_log": True
        },
        "alarm": {
            "secret": "SECdbd47e3cfb9229e69dc6ea98ae35c6e4220c8e6da50c3d7fbbcdecc12445c187",
            "url": "https://oapi.dingtalk.com/robot/send?access_token=2978d209d8667f1bfc57d985b00b7366a6d3bcbd762f2d5f128a14350e263e87",
            "atMobiles": [],
            "isAtAll": False
        }
    },
    "kaifa": {
        "log_level": {
            "console": "DEBUG",
            "file": "DEBUG",
            "third_log": True  # True 不打印
        },
        "alarm": {
            "secret": "SEC2e957a153c19f536496057f09d4e17da533d86ebb5308faf01d6ff29745aaeac",
            "url": "https://oapi.dingtalk.com/robot/send?access_token=35a35b15e741c55563c627720bc829a6aab341806d56510c8036c99f282c8694",
            "atMobiles": [],
            "isAtAll": False
        }
    }
}
