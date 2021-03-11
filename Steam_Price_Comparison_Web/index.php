<?php
$url = "http://127.0.0.1:8080/api/";
$curl = curl_init($url);
$post_url = $_POST["url"];
$post_url ??="https://store.steampowered.com/app/578080/PLAYERUNKNOWNS_BATTLEGROUNDS/";
$path = parse_url($post_url, PHP_URL_PATH);
$id = (int) filter_var($path, FILTER_SANITIZE_NUMBER_INT);
$data = json_encode(array('id' => $id));
curl_setopt($curl, CURLOPT_HEADER, false);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HTTPHEADER, array("Content-type: application/json"));
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
$response = curl_exec($curl);
curl_close($curl);
$all_data = json_decode($response,true);
?>
<html>
<header>
    <title>Steam各区比价</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, shrink-to-fit=no"/>
    <meta name="renderer" content="webkit"/>
    <meta name="force-rendering" content="webkit"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
    <meta name="description" content="Steam各区比价" />
    <meta name="keywords" content="steam,比价,steam国区,steam俄罗斯区" />
    <link href="index.css" rel="stylesheet">
    <link
        rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/mdui@1.0.1/dist/css/mdui.min.css"
        integrity="sha384-cLRrMq39HOZdvE0j6yBojO4+1PrHfB7a9l5qLcmRm/fiWXYY+CndJPmyu5FV/9Tw"
        crossorigin="anonymous"
    />
</header>
<body class="mdui-theme-accent-pink">
<div class="mdui-container">
    <form action="index.php" method="post">
        <div class="mdui-textfield">
            <label class="mdui-textfield-label">请输入Steam商店网址来查询各区价格</label>
            <input class="mdui-textfield-input" type="text" name="url" placeholder="https://store.steampowered.com/app/578080/PLAYERUNKNOWNS_BATTLEGROUNDS/" required/>
            <div class="mdui-textfield-error">网址不能为空</div>
        </div>

    <button class="mdui-btn mdui-color-theme-accent mdui-float-right" type="submit">查询</button>
    </form>
    <div class="mdui-typo">
        <?php
        print "<h1>".$all_data[0]['game_name']."<small>".$all_data[0]['appid']."</small>"."</h1>"
        ?>
    </div>
    <div class="mdui-table-fluid">
        <table class="mdui-table mdui-table-hoverable">
            <thead>
            <tr>
                <th>货币种类</th>
                <th>全球价格</th>
                <th>人民币价格</th>
                <th>最低价</th>
                <th>折后价</th>
            </tr>
            </thead>
            <tbody>
                <?php
                for ($i = 0; $i <= sizeof($all_data)-1; $i++)
                {
                    print "<tr>";
                    print "<td>".$all_data[$i]['currency']."</td>";
                    print "<td>".$all_data[$i]['currency_price']."</td>";
                    print "<td>".$all_data[$i]['converted_price']."</td>";
                    print "<td>".$all_data[$i]['lowest_price']."</td>";
                    print "<td>".$all_data[$i]['discount_minor']."</td>";
                    print "</tr>";
                }
                ?>
            </tbody>
        </table>
    </div>

</div>
<div class="mdui-container">
    <div class="mdui-typo">
        <h1>
            在线人数
            <small>
                Steam Charts
            </small>
        </h1>
    </div>
    <?php
    print '<iframe src="https://steamdb.info/embed/?appid='.$all_data[0]['appid'].'" height="389" style="border:0;overflow:hidden;width:100%"></iframe>'
    ?>
</div>


<script
        src="https://cdn.jsdelivr.net/npm/mdui@1.0.1/dist/js/mdui.min.js"
        integrity="sha384-gCMZcshYKOGRX9r6wbDrvF+TcCCswSHFucUzUPwka+Gr+uHgjlYvkABr95TCOz3A"
        crossorigin="anonymous"
></script>
</body>
<!-- 一言 -->
<script src="//v1.hitokoto.cn/?encode=js&select=%23hitokoto" defer></script>

<footer>
    <br><br><br>
    <div class="mdui-container">
        <div class="footer">
            <div class="mdui-text-center">
                <p id="hitokoto" class="footer-copyright">:D 获取中...</p>
                <div class="footer-copyright">Copyright © 2016 - 2021 <a href="https://www.xsy.fun">XSY</a> - Steam_Price_Comparison Dev Group | All rights reserved.</div>
            </div>
        </div>
    </div>
</footer>


</html>
