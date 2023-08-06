import $ from 'jquery';

window.PODCAST_CHOOSER_MODAL_ONLOAD_HANDLERS = {
  choose(modal) {
    function serializeFormData(form) {
      // Return the non-empty form data as an object
      return Object.fromEntries(
        Array.from(new FormData(form)).filter((pair) => Boolean(pair[1]))
      );
    }

    const searchForm = modal.body[0].querySelector('form.podcast-search');
    const searchResults = modal.body[0].querySelector('#search-results');
    const searchUrl = searchForm.action;
    let request;

    function ajaxifyLinks(context) {
      $('.listing a', context).on('click', function () {
        modal.loadUrl(this.href);
        return false;
      });

      $('.pagination a', context).on('click', function () {
        loadResults(this.href);
        return false;
      });
    }

    function loadResults(url, data) {
      const opts = {
        url,
        success(resultsData) {
          request = null;
          $(searchResults).html(resultsData);
          ajaxifyLinks(searchResults);
        },
        error() {
          request = null;
        },
      };
      if (data) {
        opts.data = data;
      }

      request = $.ajax(opts);
    }

    function search() {
      loadResults(searchUrl, serializeFormData(searchForm));
      return false;
    }

    $(searchForm).on('submit', search);

    $(searchForm.elements).on('input', function () {
      if (request) {
        request.abort();
      }

      clearTimeout($.data(this, 'timer'));
      const wait = setTimeout(search, 200);
      $(this).data('timer', wait);
    });

    ajaxifyLinks(modal.body);
  },
  chosen(modal, jsonData) {
    modal.respond('podcastChosen', jsonData.result);
    modal.close();
  },
};
