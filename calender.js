document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    
    if (calendarEl) {
      // Initialize the FullCalendar
      const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
        },
        themeSystem: 'bootstrap5',
        events: '/api/events',
        editable: false,
        eventTimeFormat: {
          hour: '2-digit',
          minute: '2-digit',
          meridiem: true
        },
        eventClick: function(info) {
          window.location.href = '/event/' + info.event.id;
        },
        loading: function(isLoading) {
          if (isLoading) {
            document.getElementById('loading-events').classList.remove('d-none');
          } else {
            document.getElementById('loading-events').classList.add('d-none');
          }
        },
        eventDisplay: 'block',
        eventColor: '#0dcaf0', // Bootstrap info color
        eventTextColor: '#000',
        dayMaxEvents: true, // Allow "more" link when too many events
        height: 'auto',
        eventDidMount: function(info) {
          // Add tooltips to events
          const eventEl = info.el;
          const event = info.event;
          
          const tooltip = new bootstrap.Tooltip(eventEl, {
            title: `${event.title}\nLocation: ${event.extendedProps.location || 'Not specified'}\nTime: ${event.start.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} - ${event.end.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}`,
            placement: 'top',
            trigger: 'hover',
            container: 'body'
          });
        }
      });
      
      calendar.render();
      
      // Add responsive behavior for view switching
      function handleViewChange() {
        const width = window.innerWidth;
        if (width < 768) {
          calendar.changeView('listMonth');
        } else {
          calendar.changeView('dayGridMonth');
        }
      }
      
      // Set initial view based on screen size
      handleViewChange();
      
      // Listen for window resize events
      window.addEventListener('resize', handleViewChange);
    }
  });
  
