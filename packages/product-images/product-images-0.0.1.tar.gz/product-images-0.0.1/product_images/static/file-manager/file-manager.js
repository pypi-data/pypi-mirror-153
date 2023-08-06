
FileManager = function (params) {
    var $e = findElements(params.$select),
        html = $('html');

    /* Constructor */
    renderFiles(params.initial || []);

    new Dropzone($e.dropFilesSection[0], {
        url: params.uploadUrl,
        createImageThumbnails: false,
        acceptedFiles: 'image/*',
        parallelUploads: 5,
        addedfile: function(file) {},
        success: function (file, response) {
            renderFile(response.id, response.url);
        },
        error: function (file, response) {
            console.log(response);
        }
    });

    $e.files.sortable({
        items:'.file-preview',
        cursor: 'move',
        opacity: 0.7,
        distance: 20,
        tolerance: 'pointer',
        update: function(event, ui) {
            $e.select.empty();
            $e.files.find('.file-preview').each(function () {
                addOption($(this).data('file-id'));
            });
        }
    });

    /* Events */
    html.on('dragover', stopEvent);
    html.on('dragleave', stopEvent);

    $e.dropLinkSection.on('drop', handleLinkSectionDrop);

    /* Helpers */
    function findElements($select) {
        var $c = $('[data-role=images-container]');
        return {
            select: $select,
            container: $c,
            dropLinkSection: $c.find('[data-role=drop-link-section]'),
            dropFilesSection: $c.find('[data-role=drop-files-section]'),
            files: $c.find('[data-role=files]')
        }
    }

    function renderFiles(files) {
        $e.select.empty();

        $.each(files, function () {
            renderFile(this.id, this.url);
        });
    }

    function renderFile(id, url) {
        var $file = $('<div />').addClass('file-preview').data('file-id', id),
            $img = $('<img />').prop('src', url);

        addOption(id);

        $file.append($img);

        $e.files.append($file);

        $img.dblclick(function (e) {
            if (!e.altKey || !e.ctrlKey) {
                return;
            }

            $e.select.find('option[value=' + id + ']').remove();
            $file.remove();
        });
    }

    function addOption(fileId) {
        var $option = $('<option />').prop({
                value: fileId,
                selected: true
            }).text(fileId);

        $e.select.append($option);
    }

    function handleLinkSectionDrop(event) {
        var html,
            url,
            data;

        stopEvent(event);

        html = event.originalEvent.dataTransfer.getData('text/html');
        url = $('<div />').html(html).find("img").attr('src');
        data = {url: url};

        $.post(
            params.uploadUrl,
            data
        ).success(function (response) {
            renderFile(response.id, response.url);
        }).fail(function (response) {
            console.log(response);
        });
    }

    function stopEvent(event) {
        event.preventDefault();
        event.stopPropagation();
    }

};
