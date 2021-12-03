# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/29
# @Author  : MashiroF
# @File    : HT_account.py
# @Software: PyCharm

## 账号管理样本
# {
#     'user':'空白',        # 备注,必要
#     'CK':'memberinfo=%7B%22id%22%3A%22816727988%22%2C%22name%22%3A%22%E7%94%A8%E6%88%B701726742289%22%2C%22oid%22%3A%22NWZLVGorR2FRQ0pGQVNKc2RJRWwvdz09%22%7D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22NWZLVGorR2FRQ0pGQVNKc2RJRWwvdz09%22%2C%22%24device_id%22%3A%2217d7faeb00622b-043d940d606bfc-346c0420-304704-17d7faeb0072%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22NWZLVGorR2FRQ0pGQVNKc2RJRWwvdz09%22%7D; uc=direct; um=task; us=qiandao; ut=direct; utm_campaign=direct; utm_medium=direct; utm_source=direct; utm_term=direct; _ga_nefid_=ERS0MMsw1e5AUhRQRAdvpj%2Fqje2b0sNS; ENCODE_TOKENSID=; Personalized=1; TOKENSID=TOKEN_eyJhbGciOiJFQ0RTQSIsInYiOiIxIn0.eyJleHAiOjE2NDExMTY2NzY5NDQsImlkIjoiODE2NzI3OTg4IiwiaWRjIjoic2hvdW1pbmciLCJ0aWQiOiJPQnpmUWpoUGFSRTVrTHdoTUs4UVVuVHJJWjdxeWs0M0Ewa3dLTFUrUFpMTmJGUjE4QzVYaXlwOVBENGxqOGdKanFzWDMwaXQ5TEFBZTJFdC9QRXFhNEVDSWZEOUhBaWtNdWpTeStkd05FQT0ifQ.MEYCIQCKQUMrLzxhoBH0lPbPYhnJfibKfDunEL9GDkIl39sDNQIhALD80DxmLiQ8yh2y4znLGXDS92MZ85rmaDyc3TEnnvoO; apkPkg=com.oppo.store; app_innerutm={"uc":"direct","um":"direct","ut":"direct","us":"direct"}; app_param={"appKey":"","romVersion":"14.3","rom":"iOS","sa_device_id":"2968D82D-070E-4F43-A0B6-C1E787C03A49","apkPkg":"com.oppo.store","model":"iPhone9,2","appId":"","brand":"iPhone","guid":"2968D82D-070E-4F43-A0B6-C1E787C03A49"}; app_utm={"utm_source_app":"direct","utm_campaign_app":"direct","utm_term_app":"direct","utm_medium_app":"direct"}; exp_id=; experiment_id=4181_1006_1492_-1510_476_74_-105_1066_-1071_1_325_2_2_739_-568_261_4_11_17_2_1_61_68_23_5_3_5_2_3_3_4_2_2_8_2_2_8_3_1_34_1_3_26_-9_86_2_9_2_2_9_2_14_1_6_42_2_77_1_37; log_id=; referer=; retrieve_id=; s_channel=ios_oppostore; s_version=300002; sa_distinct_id=NWZLVGorR2FRQ0pGQVNKc2RJRWwvdz09; scene_id=; section_id=; source_type=505; strategy_id=; acw_tc=2760778916385266412067856ea876da6eb2a4fdc089a5585edfc46b96fe97; oppostore_rsa_key=MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJCYMLNhFBtDcbb72YZVDm%2FFG3m3oR4kU8f7JgvAmhI%2FlQvqhYczoJz8QZU30ml0nvtO2dB%2FfcqTEW9RyUhw8jUCAwEAAQ%3D%3D; sajssdk_2015_cross_new_user=1',          # Cookie,必要(建议全部粘贴)
#     'UA':''           # User-Agent,必要
# },

## 账号管理
accounts = [
    {
        'user':'525',
        'CK':'memberinfo=%7B%22id%22%3A%22816727988%22%2C%22name%22%3A%22%E7%94%A8%E6%88%B701726742289%22%2C%22oid%22%3A%22NWZLVGorR2FRQ0pGQVNKc2RJRWwvdz09%22%7D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22NWZLVGorR2FRQ0pGQVNKc2RJRWwvdz09%22%2C%22%24device_id%22%3A%2217d7faeb00622b-043d940d606bfc-346c0420-304704-17d7faeb0072%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22NWZLVGorR2FRQ0pGQVNKc2RJRWwvdz09%22%7D; uc=direct; um=task; us=qiandao; ut=direct; utm_campaign=direct; utm_medium=direct; utm_source=direct; utm_term=direct; _ga_nefid_=ERS0MMsw1e5AUhRQRAdvpj%2Fqje2b0sNS; ENCODE_TOKENSID=; Personalized=1; TOKENSID=TOKEN_eyJhbGciOiJFQ0RTQSIsInYiOiIxIn0.eyJleHAiOjE2NDExMTY2NzY5NDQsImlkIjoiODE2NzI3OTg4IiwiaWRjIjoic2hvdW1pbmciLCJ0aWQiOiJPQnpmUWpoUGFSRTVrTHdoTUs4UVVuVHJJWjdxeWs0M0Ewa3dLTFUrUFpMTmJGUjE4QzVYaXlwOVBENGxqOGdKanFzWDMwaXQ5TEFBZTJFdC9QRXFhNEVDSWZEOUhBaWtNdWpTeStkd05FQT0ifQ.MEYCIQCKQUMrLzxhoBH0lPbPYhnJfibKfDunEL9GDkIl39sDNQIhALD80DxmLiQ8yh2y4znLGXDS92MZ85rmaDyc3TEnnvoO; apkPkg=com.oppo.store; app_innerutm={"uc":"direct","um":"direct","ut":"direct","us":"direct"}; app_param={"appKey":"","romVersion":"14.3","rom":"iOS","sa_device_id":"2968D82D-070E-4F43-A0B6-C1E787C03A49","apkPkg":"com.oppo.store","model":"iPhone9,2","appId":"","brand":"iPhone","guid":"2968D82D-070E-4F43-A0B6-C1E787C03A49"}; app_utm={"utm_source_app":"direct","utm_campaign_app":"direct","utm_term_app":"direct","utm_medium_app":"direct"}; exp_id=; experiment_id=4181_1006_1492_-1510_476_74_-105_1066_-1071_1_325_2_2_739_-568_261_4_11_17_2_1_61_68_23_5_3_5_2_3_3_4_2_2_8_2_2_8_3_1_34_1_3_26_-9_86_2_9_2_2_9_2_14_1_6_42_2_77_1_37; log_id=; referer=; retrieve_id=; s_channel=ios_oppostore; s_version=300002; sa_distinct_id=NWZLVGorR2FRQ0pGQVNKc2RJRWwvdz09; scene_id=; section_id=; source_type=505; strategy_id=; acw_tc=2760778916385266412067856ea876da6eb2a4fdc089a5585edfc46b96fe97; oppostore_rsa_key=MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJCYMLNhFBtDcbb72YZVDm%2FFG3m3oR4kU8f7JgvAmhI%2FlQvqhYczoJz8QZU30ml0nvtO2dB%2FfcqTEW9RyUhw8jUCAwEAAQ%3D%3D; sajssdk_2015_cross_new_user=1',
        'UA':'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 oppostore/300002 IOS/14.3 brand/iPhone model/iPhone9,2'
    },
    {
        'user':'',
        'CK':'',
        'UA':''
    },
]
