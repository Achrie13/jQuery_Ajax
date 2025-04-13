var baseUrl = "http://127.0.0.1:8000"; // API 基础地址

function getCategory() {
  $.ajax({
    url: baseUrl + "/category", // API 请求路径
    type: "GET",
    async: false,
    cache: false, // 不缓存
    dataType: "json",
    beforeSend: function () {
      // 请求前的处理
      $("#CategoryId").empty();
    },
    success: function (data) {
      // 请求成功的处理
      if (Array.isArray(data)) {
        $("#CategoryId").append(
          '<option value="-1" selected="true">--请选择型号--</option>'
        );
        for (var i = 0; i < data.length; i++) {
          $("#CategoryId").append(
            '<option value="' +
              data[i].CategoryId +
              '">' +
              data[i].CategoryName +
              "</option>"
          );
        }
        // alert("加载成功!");
      }
    },
    complete: function (XMLHttpRequest, status) {
      // 请求完成后的处理
      if (status === "timeout") {
        alert("请求超时!");
        ajaxTimeout.abort();
      }
    },
    error: function () {
      // 请求出错的处理
      alert("加载类别失败!");
    },
  });
}

function getProducts(CategoryID) {
  $.ajax({
    url: baseUrl + "/category/" + CategoryID,
    type: "GET",
    async: false,
    cache: false,
    dataType: "json",
    beforeSend: function () {
      $("#ProductId").empty();
    },
    success: function (data) {
      if (Array.isArray(data)) {
        $("#ProductId").append(
          '<option value="-1" selected="true">--请选择产品--</option>'
        );
        for (var i = 0; i < data.length; i++) {
          $("#ProductId").append(
            '<option value="' +
              data[i].ProductId +
              '">' +
              data[i].ProductName +
              "</option>"
          );
        }
        // alert("加载成功!");
      }
    },
    complete: function (XMLHttpRequest, status) {
      // 请求完成后的处理
      if (status === "timeout") {
        alert("请求超时!");
        ajaxTimeout.abort();
      }
    },
    error: function () {
      // 请求出错的处理
      alert("加载产品失败!");
    },
  });
}

function load_data_1(ProductID) {
  $.ajax({
    url: baseUrl + "/product/" + ProductID,
    type: "GET",
    dataType: "json",
    success: function (data) {
      const xData = data.map((item) => item.ShipCountry);
      const yData = data.map((item) => item.sales_quantity);
      const chartDom = document.getElementById("chart_1");
      const existingChart = echarts.getInstanceByDom(chartDom);
      if (existingChart) {
        echarts.dispose(chartDom);
      }

      const myChart = echarts.init(chartDom);

      const option = {
        title: { text: "产品各国销量统计" },
        tooltip: {},
        xAxis: {
          type: "category",
          data: xData,
          axisLabel: {
            rotate: 45,
            margin: 15,
            interval: 0,
          },
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            name: "销量",
            data: yData,
            type: "bar",
          },
        ],
      };

      myChart.setOption(option);
    },
    error: function () {
      alert("加载图表数据失败！");
    },
  });
}

function load_data_2() {
  $.ajax({
    url: baseUrl + "/query/1",
    type: "GET",
    dataType: "json",
    success: function (data) {
      const xData = data.map((item) => item.ProductName);
      const yData = data.map((item) => item.TotalSales);
      const chartDom = document.getElementById("chart_2");
      const existingChart = echarts.getInstanceByDom(chartDom);
      if (existingChart) {
        echarts.dispose(chartDom);
      }

      const myChart = echarts.init(chartDom);

      const option = {
        title: { text: "产品销量前十统计" },
        tooltip: {},
        xAxis: {
          type: "category",
          data: xData,
          axisLabel: {
            rotate: 45,
            margin: 15,
            interval: 0,
          },
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            name: "销量",
            data: yData,
            type: "bar",
          },
        ],
      };

      myChart.setOption(option);
    },
    error: function () {
      alert("加载图表数据失败！");
    },
  });
}

