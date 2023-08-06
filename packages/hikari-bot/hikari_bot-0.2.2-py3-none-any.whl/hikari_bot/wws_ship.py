from typing import List
import httpx
import traceback
import jinja2
import re
import asyncio
from pathlib import Path
from .data_source import servers,set_shipparams,tiers
from .utils import match_keywords
from nonebot_plugin_htmlrender import html_to_pic,text_to_pic
from nonebot.adapters.onebot.v11 import MessageSegment
from.publicAPI import get_ship_byName,get_AccountIdByName
from collections import defaultdict, namedtuple
from nonebot import get_driver
from nonebot.log import logger

dir_path = Path(__file__).parent
template_path = dir_path / "template"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path), enable_async=True
)

headers = {
    'Authorization': get_driver().config.api_token
}

ShipSlectState = namedtuple("ShipSlectState", ['state','SlectIndex','SelectList'])
SecletProcess = defaultdict(lambda: ShipSlectState(False, None, None))

async def get_ShipInfo(qqid,info,bot):
    try:
        url,params = '',''
        if isinstance(info,List):
            for flag,i in enumerate(info):              #是否包含me或@，包含则调用平台接口
                if i == 'me':
                    url = 'https://api.wows.linxun.link/public/wows/account/v2/ship/info'
                    params = {
                    "server": "QQ",
                    "accountId": qqid,
                    }
                    info.remove("me")
                match = re.search(r"CQ:at,qq=(\d+)",i)
                if match:
                    url = 'https://api.wows.linxun.link/public/wows/account/v2/ship/info'
                    params = {
                    "server": "QQ",
                    "accountId": match.group(1),
                    }
                    info[flag] = str(i).replace(f"[{match.group(0)}]",'')
                    if not info[flag]:
                        info.remove('')
                    break
            if not params and len(info) == 3:
                param_server,info = await match_keywords(info,servers)
                if param_server:
                    param_accountid = await get_AccountIdByName(param_server,str(info[0]))      #剩余列表第一个是否为游戏名
                    if param_accountid and param_accountid != 404:
                        info.remove(info[0])
                        url = 'https://api.wows.linxun.link/public/wows/account/v2/ship/info'
                        params = {
                        "server": param_server,
                        "accountId": param_accountid,
                        }
                    elif param_accountid == 404:
                        return '无法查询该游戏昵称Orz，请检查昵称是否存在'
                    else:
                        return '发生了错误，有可能是网络波动，请稍后再试'
                else:
                    return '服务器参数似乎输错了呢'
            elif params:
                print(params)
            else:
                return '您似乎准备用游戏昵称查询单船战绩，请检查参数中是否包含服务器、游戏昵称和船名，以空格区分'
            shipList = await get_ship_byName(str(info[0]))
            print(shipList)
            if shipList:
                if len(shipList) < 2:
                    params["shipId"] = shipList[0][0]
                else:
                    msg = f'存在多条名字相似的船\n请在20秒内选择对应的序号\n=================\n'
                    flag = 0
                    for each in shipList:
                        flag += 1
                        msg += f"{flag}：{tiers[each[3]-1]} {each[1]}\n"
                    SecletProcess[qqid] = ShipSlectState(False, None, shipList)
                    img = await text_to_pic(text=msg,width=230)
                    await bot.send(MessageSegment.image(img))
                    a = 0
                    while a < 200 and not SecletProcess[qqid].state:
                        a += 1
                        await asyncio.sleep(0.1)
                    if SecletProcess[qqid].state and SecletProcess[qqid].SlectIndex <= len(shipList):
                        params["shipId"] = shipList[SecletProcess[qqid].SlectIndex-1][0]
                    else:
                        return '已超时退出'
            else:
                return '找不到船'
        else:
            return '参数似乎出了问题呢'
        logger.info(f"下面是本次请求的参数，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{url}\n{params}")
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=20)
            logger.info(f"下面是本次请求返回的状态码，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{resp.status_code}")
            result = resp.json()
        if result['code'] == 200 and result['data']:
            template = env.get_template("wws-ship.html")
            template_data = await set_shipparams(result['data'])
            content = await template.render_async(template_data)
            return await html_to_pic(content, wait=0, viewport={"width": 800, "height": 100})
        elif result['code'] == 403:
            return f"{result['message']}\n请先绑定账号"
        elif result['code'] == 404:
            return f"{result['message']}"
        elif result['code'] == 500:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
        else:
            return 'wuwuu好像出了点问题，可能是网络问题，过一会儿还是不行的话请联系麻麻~'
    except Exception:
        logger.error(traceback.format_exc())
        return 'wuwuu好像出了点问题，过一会儿还是不行的话请联系麻麻~'