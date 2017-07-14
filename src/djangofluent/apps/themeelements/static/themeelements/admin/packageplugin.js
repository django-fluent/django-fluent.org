(function($){

    function getRtdInfo(event) {
        // The fun. Just because we can.
        // Fetch the other fields when the project is on read the docs.
        var slug = event.target.value;
        if(! slug)
            return;

        var $root = $(event.target).closest('.inline-related');

        // Thank you OpenComparison
        $.ajax({
            url: 'http://readthedocs.org/api/v1/project/' + slug + '/?format=jsonp',
            dataType: 'jsonp',
            success: function(data) {
                var $description = $root.find('.form-row.description textarea');
                var $repository_url = $root.find('.form-row.repository_url input');
                var $homepage = $root.find('.form-row.homepage input');
                var repo_url = data.repo.replace(/\.git$/, '');   // Might be added in RTD

                if(! $repository_url.val()) $repository_url.val(repo_url);
                if(! $homepage.val() && repo_url != data.project_url)
                    $homepage.val(data.project_url);

                if(! $description.val()) {
                    var rtd_description = data.description.substring(0,300);
                    rtd_description = rtd_description.substring(0, rtd_description.lastIndexOf('\n') + 1);

                    // Also see if a shorter summary can be fetched from GitHub
                    if(data.repo.indexOf('github.com/') != -1) {
                        _setGitHubDescription($description, repo_url, rtd_description);
                    }
                    else {
                        $description.val(rtd_description);
                    }
                }
            }
        });
    }

    function getRepositoryInfo(event) {
        var repo_url = event.target.value;
        if(! repo_url)
            return;

        var $root = $(event.target).closest('.inline-related');
        var $description = $root.find('.form-row.description textarea');
        if($description.val())
            return;

        if(repo_url.indexOf('github.com/') != -1) {
            _setGitHubDescription($description, repo_url);
        }
    }

    function _setGitHubDescription($description, repo_url, fallback) {
        repo_url = repo_url.replace(/\.git$/, '');
        var repo = repo_url.split('/');

        $.ajax({
            url: 'https://api.github.com/repos/' + repo[3] + '/' + repo[4],
            dataType: 'jsonp',
            success: function(data) {
                $description.val(data.data.description);
                var $slug = $description.closest('.inline-related').find('.form-row.slug input');
                if(! $slug.val()) $slug.val(data.data.name);   // I got really lazy here :)
            },
            error: function(data) {
                if(fallback) $description.val(fallback);
            }
        });
    }


    // Make sure the WYSIWYG editor is loaded for our models.
    fluent_contents.plugins.registerViewHandler('PackageItem', {
        'enable': function enablePackageItem($root) {
            $root.find('.form-row.slug input').change(getRtdInfo);
            $root.find('.form-row.repository_url input').change(getRepositoryInfo);
        },
        'disable': function($root) {}
    });

})(window.jQuery || django.jQuery);
