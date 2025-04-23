// Confirm deletion
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-event');
    
    deleteButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        if (!confirm('Are you sure you want to delete this event? This action cannot be undone.')) {
          e.preventDefault();
        }
      });
    });
  
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
      setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      }, 5000);
    });
  });
  
  // Form validation
  function validateEventForm() {
    const startTime = new Date(document.getElementById('start_time').value);
    const endTime = new Date(document.getElementById('end_time').value);
    
    if (endTime <= startTime) {
      alert('End time must be after start time');
      return false;
    }
    
    return true;
  }
  
  // Toggle between calendar and list views
  function toggleView(view) {
    const calendarView = document.getElementById('calendar-view');
    const listView = document.getElementById('list-view');
    const calendarBtn = document.getElementById('calendar-btn');
    const listBtn = document.getElementById('list-btn');
    
    if (view === 'calendar') {
      calendarView.classList.remove('d-none');
      listView.classList.add('d-none');
      calendarBtn.classList.add('active');
      listBtn.classList.remove('active');
    } else {
      calendarView.classList.add('d-none');
      listView.classList.remove('d-none');
      calendarBtn.classList.remove('active');
      listBtn.classList.add('active');
    }
  }
  
