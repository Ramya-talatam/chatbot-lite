document.getElementById('settings-icon').addEventListener('click', function() {
    event.preventDefault();
          document.getElementById('themeModal').style.display = 'block';
      });

      document.getElementsByClassName('close')[0].addEventListener('click', function() {
          document.getElementById('themeModal').style.display = 'none';
      });

      document.getElementById('theme-select').addEventListener('change', function() {
          var theme = this.value;
          document.getElementById('theme-link').href = theme;
      });