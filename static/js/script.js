const menuItems = document.querySelectorAll(".menu-item");
const pages = document.querySelectorAll(".page");

let priorityChartCreated = false;
let categoryChartCreated = false;
let hourChartCreated = false;

let slaChartCreated = false;
let slaRateChartCreated = false;

let resolutionPriorityChartCreated = false;
let monthlyResolutionChartCreated = false;
let longestIncidentChartCreated = false;

let teamChartCreated = false;
let employeeChartCreated = false;
let teamResolutionChartCreated = false;

menuItems.forEach((item) => {
  item.addEventListener("click", function (e) {
    e.preventDefault();

    // Sayfaları gizle

    pages.forEach((page) => {
      page.style.display = "none";
    });

    // Menü aktif temizleme

    menuItems.forEach((link) => {
      link.classList.remove("active");
    });

    // Seçilen sayfa

    const selectedPage = document.getElementById(this.dataset.page);

    if (selectedPage) {
      selectedPage.style.display = "block";
    }

    this.classList.add("active");

    // OPERASYON ANALİZİ

    if (this.dataset.page === "operasyon") {
      // Priority Grafik

      if (!priorityChartCreated) {
        const ctx = document.getElementById("priorityChart");

        const data = JSON.parse(
          document.getElementById("priority-data").textContent,
        );

        new Chart(ctx, {
          type: "bar",

          data: {
            labels: Object.keys(data),

            datasets: [
              {
                label: "Incident Sayısı",

                data: Object.values(data),
              },
            ],
          },

          options: {
            responsive: true,
          },
        });

        priorityChartCreated = true;
      }

      // Kategori Grafik

      if (!categoryChartCreated) {
        const ctx = document.getElementById("categoryChart");

        const data = JSON.parse(
          document.getElementById("category-data").textContent,
        );

        new Chart(ctx, {
          type: "bar",

          data: {
            labels: Object.keys(data),

            datasets: [
              {
                label: "Kategori Sayısı",

                data: Object.values(data),
              },
            ],
          },

          options: {
            responsive: true,
          },
        });

        categoryChartCreated = true;
      }

      // Yoğun Saat Grafik

      if (!hourChartCreated) {
        const ctx = document.getElementById("hourChart");

        const data = JSON.parse(
          document.getElementById("hour-data").textContent,
        );

        new Chart(ctx, {
          type: "line",

          data: {
            labels: Object.keys(data),

            datasets: [
              {
                label: "Saatlik Incident",

                data: Object.values(data),
              },
            ],
          },

          options: {
            responsive: true,
          },
        });

        hourChartCreated = true;
      }

      // =========================
      // SLA GRAFİKLERİ
      // =========================

      if (!slaChartCreated) {
        const ctx = document.getElementById("slaChart");

        const data = JSON.parse(
          document.getElementById("sla-rate-data").textContent,
        );

        new Chart(ctx, {
          type: "bar",

          data: {
            labels: Object.keys(data),

            datasets: [
              {
                label: "SLA Durumu",

                data: Object.values(data),
              },
            ],
          },

          options: {
            responsive: true,
            maintainAspectRatio: false,
          },
        });

        slaChartCreated = true;
      }

      // SLA Başarı Oranı

      if (!slaRateChartCreated) {
        const ctx = document.getElementById("slaRateChart");

        const data = JSON.parse(
          document.getElementById("sla-rate-data").textContent,
        );

        new Chart(ctx, {
          type: "pie",

          data: {
            labels: Object.keys(data),

            datasets: [
              {
                label: "SLA Oranı",

                data: Object.values(data),
              },
            ],
          },

          options: {
            responsive: true,
            maintainAspectRatio: false,
          },
        });

        slaRateChartCreated = true;
      }
    }

    // =========================
    // SÜRE ANALİZİ
    // =========================

    if (this.dataset.page === "sure") {
      if (!resolutionPriorityChartCreated) {
        const ctx = document.getElementById("resolutionPriorityChart");

        const data = JSON.parse(
          document.getElementById("resolution-priority-data").textContent,
        );

        new Chart(ctx, {
          type: "bar",

          data: {
            labels: Object.keys(data),

            datasets: [
              {
                label: "Ortalama Çözüm Süresi (Saat)",

                data: Object.values(data),
              },
            ],
          },

          options: {
            responsive: true,
          },
        });

        resolutionPriorityChartCreated = true;
      }

      if (!monthlyResolutionChartCreated) {
        const ctx = document.getElementById("monthlyResolutionChart");

        const data = JSON.parse(
          document.getElementById("monthly-resolution-data").textContent,
        );

        new Chart(ctx, {
          type: "line",

          data: {
            labels: Object.keys(data),

            datasets: [
              {
                label: "Aylık Ortalama Süre",

                data: Object.values(data),
              },
            ],
          },

          options: {
            responsive: true,
          },
        });

        monthlyResolutionChartCreated = true;
      }

      if (!longestIncidentChartCreated) {
        const ctx = document.getElementById("longestIncidentChart");

        const data = JSON.parse(
          document.getElementById("longest-incidents-data").textContent,
        );

        new Chart(ctx, {
          type: "bar",

          data: {
            labels: Object.keys(data),

            datasets: [
              {
                label: "Çözüm Süresi Saat",

                data: Object.values(data),
              },
            ],
          },

          options: {
            responsive: true,
          },
        });

        longestIncidentChartCreated = true;
      }
    }

    // =========================
    // EKİP ANALİZİ
    // =========================

    if (this.dataset.page === "ekip") {
      if (!teamChartCreated) {
        const ctx = document.getElementById("teamChart");

        const data = JSON.parse(
          document.getElementById("team-data").textContent,
        );

        new Chart(ctx, {
          type: "bar",

          data: {
            labels: Object.keys(data),

            datasets: [
              {
                label: "Incident Sayısı",

                data: Object.values(data),
              },
            ],
          },

          options: {
            responsive: true,
          },
        });

        teamChartCreated = true;
      }

      if (!employeeChartCreated) {
        const ctx = document.getElementById("employeeChart");

        const data = JSON.parse(
          document.getElementById("employee-data").textContent,
        );

        new Chart(ctx, {
          type: "bar",

          data: {
            labels: Object.keys(data),

            datasets: [
              {
                label: "Çalışan Performansı",

                data: Object.values(data),
              },
            ],
          },

          options: {
            responsive: true,
          },
        });

        employeeChartCreated = true;
      }

      if (!teamResolutionChartCreated) {
        const ctx = document.getElementById("teamResolutionChart");

        const data = JSON.parse(
          document.getElementById("team-resolution-data").textContent,
        );

        new Chart(ctx, {
          type: "bar",

          data: {
            labels: Object.keys(data),

            datasets: [
              {
                label: "Ortalama Çözüm Süresi Saat",

                data: Object.values(data),
              },
            ],
          },

          options: {
            responsive: true,
          },
        });

        teamResolutionChartCreated = true;
      }
    }
  });
});

// İlk açılış

pages.forEach((page) => {
  page.style.display = "none";
});

if (activePage) {
  pages.forEach((page) => {
    page.style.display = "none";
  });

  document.getElementById(activePage).style.display = "block";

  menuItems.forEach((item) => {
    item.classList.remove("active");
  });

  document.querySelector(`[data-page="${activePage}"]`).classList.add("active");
} else {
  document.getElementById("genel").style.display = "block";
}
