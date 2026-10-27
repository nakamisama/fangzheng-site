/* 方正贤良工作室 · 站点交互
   无依赖，约 2KB。所有内容在 JS 失效时依然可读。 */
(function () {
  "use strict";

  var doc = document;
  doc.documentElement.classList.add("js-ready");

  /* 页头：滚过卷首后压紧 */
  var head = doc.querySelector(".site-head");
  if (head) {
    var onScroll = function () {
      head.classList.toggle("is-stuck", window.scrollY > 40);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* 章节元素进入视口后显现 */
  var items = doc.querySelectorAll(".sec .reveal");
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reduced || !("IntersectionObserver" in window)) {
    items.forEach(function (el) {
      el.classList.add("is-in");
    });
  } else {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -12% 0px", threshold: 0.12 }
    );
    items.forEach(function (el) {
      io.observe(el);
    });
  }

  /* 年份 */
  var year = doc.getElementById("year");
  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  /* 锚点跳转后把焦点交给目标章节，键盘用户不迷失 */
  doc.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function () {
      var id = link.getAttribute("href").slice(1);
      if (!id) return;
      var target = doc.getElementById(id);
      if (!target) return;
      target.setAttribute("tabindex", "-1");
      setTimeout(function () {
        target.focus({ preventScroll: true });
      }, 420);
    });
  });
})();
