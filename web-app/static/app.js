$(document).ready(function () {
    function update_status() {
        total = $('.img-preview').length
        unchecked = $('.unchecked').length
        $('#span-selected').html('Sel: ' + (total - unchecked) + ' of ' + total)
    }
    $(document).on('click', '.img-preview', function (e) {
        $(e.target).toggleClass('unchecked')
        update_status()
    })

    $(document).on('click', '#btn-check', function (e) {
        $('.img-preview').removeClass('unchecked')
        update_status()
    })

    $(document).on('click', '#btn-uncheck', function (e) {
        $('.img-preview').addClass('unchecked')
        update_status()
    })

    $(document).on('click', '#btn-clear', function (e) {
        $('#div-img-preview').html('')
        update_status()
    })


    // -------------- SEARCH BUTTON -------------------
    $('#btn-search').on('click', function () {
        $.ajax({
            url: '/search',
            type: "post",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                max_download: $('#input-max_download').val(),
                query: $('#input-query').val(),
                tags: $('#input-tags').val()
            }),
            beforeSend: function () {
                $(".overlay").show()
            },
        }).done(function (jsondata, textStatus, jqXHR) {
            result = jsondata.result
            for (i = 0; i < result.length; i++) {
                src = result[i]
                $('#div-img-preview').append(`<div class="img-container"><img src="${src}" class="img-preview"></div>`)
            }
            $('.img-preview').anarchytip();
            $(".overlay").hide()
            update_status()
        }).fail(function (jsondata, textStatus, jqXHR) {
            console.log(jsondata)
            $(".overlay").hide()
        });
    })

    // -------------- DOWNLOAD BUTTON -------------------
    $('#btn-download').on('click', function () {
        checked = []
        $('.img-preview').each(function (e) {
            if ($(this).hasClass('unchecked') == false) {
                checked.push($(this).attr('src'))
            }
        })
        if (checked.length > 0) {
            $.ajax({
                url: '/download',
                type: "post",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify({
                    links: checked,
                    scale_w: $('#input-w').val(),
                    scale_h: $('#input-h').val(),
                    tags: $('#input-tags').val()

                }),
                beforeSend: function () {
                    $(".overlay").show()
                },
            }).done(function (jsondata, textStatus, jqXHR) {
                url = jsondata.result
                window.open(url, target = "blank")

                $(".overlay").hide()
            }).fail(function (jsondata, textStatus, jqXHR) {
                console.log(jsondata)
                $(".overlay").hide()
            });
        }
    })

})