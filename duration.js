!(function () {
  // 前面补零
  function prefixInteger(num, n) {
    return (Array(n).join(0) + num).slice(-n);
  }

  // 计时起始时间，仿照格式自行修改
  var start = Date.parse("2021-07-10T16:03:05");

  function update() {
    var now = Date.now() + 250;
    var interval = (now - start) / 1000;
    var days = Math.floor(interval / 60 / 60 / 24);
    var hours = Math.floor((interval / 60 / 60) % 24);
    var minutes = Math.floor((interval / 60) % 60);
    var seconds = Math.floor(interval % 60);

    hours = prefixInteger(hours, 2);
    minutes = prefixInteger(minutes, 2);
    seconds = prefixInteger(seconds, 2);

    document.getElementById(
      "website-duration"
    ).innerHTML = `本站已运行 ${days} 天 ${hours} 小时 ${minutes} 分 ${seconds} 秒`;
  }

  update();
  setInterval(update, 250);
})();
<link rel="stylesheet" href="/css/spoiler.css" type="text/css"><script src="/js/spoiler.js" type="text/javascript" async></script>