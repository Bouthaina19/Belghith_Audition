document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.querySelector('.sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');
  
    if (toggleBtn && sidebar && mainContent) {
      toggleBtn.addEventListener('click', function() {
        if (window.innerWidth < 768) {
          // Sur mobile, on veut que le sidebar prenne toute la largeur
          sidebar.classList.toggle('mobile-open');
          document.body.classList.toggle('no-scroll');
        } else {
          // Sur desktop, comportement normal avec largeur réduite
          sidebar.classList.toggle('collapsed');
          mainContent.classList.toggle('collapsed');
        }
        this.classList.toggle('active');
        localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
      });
  
      if (localStorage.getItem('sidebarCollapsed') === 'true' && window.innerWidth >= 768) {
        sidebar.classList.add('collapsed');
        mainContent.classList.add('collapsed');
        toggleBtn.classList.add('active');
      }
    }
  
    const submenuTriggers = document.querySelectorAll('.submenu-trigger');
    
    submenuTriggers.forEach(trigger => {
      trigger.addEventListener('click', function(e) {
        e.stopPropagation();
        const parentItem = this.closest('.sidebar-item');
        parentItem.classList.toggle('open');
        
        document.querySelectorAll('.sidebar-item.with-submenu').forEach(item => {
          if (item !== parentItem) {
            item.classList.remove('open');
          }
        });
      });
    });
  });