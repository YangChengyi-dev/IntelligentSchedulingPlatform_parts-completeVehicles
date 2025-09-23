<!--  -->
<template>
  <div class="dialogDiv">
    <el-dialog class="dialog" :title="title" :visible.sync="open" :width="width" :close-on-click-modal="false"
      append-to-body :lock-scroll="false" @destroy-on-close="true">
      <el-form :model="form" :rules="rules" ref="form" class="demo-form" id="form">
        <el-form-item class="form-item" label="上级菜单:" prop="parentMenu">
          <el-input v-model="form.parentMenu" @focus="treeDialogFun"></el-input>
        </el-form-item>
        <el-form-item label="菜单类型:" prop="menuType">
          <el-radio-group v-model="form.menuType">
            <el-radio label="M">目录</el-radio>
            <el-radio label="C">菜单</el-radio>
            <el-radio label="F">按钮</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item class="form-item" label="菜单名称:" prop="menuName">
          <el-input v-model="form.menuName"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="请求地址:" prop="url">
          <el-input v-model="form.url"></el-input>
        </el-form-item>
        <el-form-item label="打开方式:" prop="target">
          <el-select v-model="form.target" placeholder="请选择">
            <el-option label="页签" value="menuItem"></el-option>
            <el-option label="新窗口" value="menuBlank"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item class="form-item" label="权限标识:" prop="perms">
          <el-input v-model="form.perms"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="显示排序:" prop="orderNum">
          <el-input v-model="form.orderNum"></el-input>
        </el-form-item>

        <el-form-item class="form-item" label="图标:" prop="icon">
          <el-input v-model="form.icon" @focus="isShowIcon = true"></el-input>
          <div class="ms-parent" style="width: 100%">
            <div class="icon-drop animated flipInX" v-show="isShowIcon" style="max-height: 200px; overflow-y: auto">
              <div class="ico-list" @click="getIcon">
                <i class="fa fa-address-book" aria-hidden="true"></i>

                <i class="fa fa-address-book-o" aria-hidden="true"></i>

                <i class="fa fa-address-card" aria-hidden="true"></i>

                <i class="fa fa-address-card-o" aria-hidden="true"></i>

                <i class="fa fa-adjust" aria-hidden="true"></i>

                <i class="fa fa-american-sign-language-interpreting" aria-hidden="true"></i>

                <i class="fa fa-anchor" aria-hidden="true"></i>

                <i class="fa fa-archive" aria-hidden="true"></i>

                <i class="fa fa-area-chart" aria-hidden="true"></i>

                <i class="fa fa-arrows" aria-hidden="true"></i>

                <i class="fa fa-arrows-h" aria-hidden="true"></i>

                <i class="fa fa-arrows-v" aria-hidden="true"></i>

                <i class="fa fa-asl-interpreting" aria-hidden="true"></i>

                <i class="fa fa-assistive-listening-systems" aria-hidden="true"></i>

                <i class="fa fa-asterisk" aria-hidden="true"></i>

                <i class="fa fa-at" aria-hidden="true"></i>

                <i class="fa fa-audio-description" aria-hidden="true"></i>

                <i class="fa fa-automobile" aria-hidden="true"></i>

                <i class="fa fa-balance-scale" aria-hidden="true"></i>

                <i class="fa fa-ban" aria-hidden="true"></i>

                <i class="fa fa-bank" aria-hidden="true"></i>

                <i class="fa fa-bar-chart" aria-hidden="true"></i>

                <i class="fa fa-bar-chart-o" aria-hidden="true"></i>

                <i class="fa fa-barcode" aria-hidden="true"></i>

                <i class="fa fa-bars" aria-hidden="true"></i>

                <i class="fa fa-bath" aria-hidden="true"></i>

                <i class="fa fa-bathtub" aria-hidden="true"></i>

                <i class="fa fa-battery" aria-hidden="true"></i>

                <i class="fa fa-battery-0" aria-hidden="true"></i>

                <i class="fa fa-battery-1" aria-hidden="true"></i>

                <i class="fa fa-battery-2" aria-hidden="true"></i>

                <i class="fa fa-battery-3" aria-hidden="true"></i>

                <i class="fa fa-battery-4" aria-hidden="true"></i>

                <i class="fa fa-battery-empty" aria-hidden="true"></i>

                <i class="fa fa-battery-full" aria-hidden="true"></i>

                <i class="fa fa-battery-half" aria-hidden="true"></i>

                <i class="fa fa-battery-quarter" aria-hidden="true"></i>

                <i class="fa fa-battery-three-quarters" aria-hidden="true"></i>

                <i class="fa fa-bed" aria-hidden="true"></i>

                <i class="fa fa-beer" aria-hidden="true"></i>

                <i class="fa fa-bell" aria-hidden="true"></i>

                <i class="fa fa-bell-o" aria-hidden="true"></i>

                <i class="fa fa-bell-slash" aria-hidden="true"></i>

                <i class="fa fa-bell-slash-o" aria-hidden="true"></i>

                <i class="fa fa-bicycle" aria-hidden="true"></i>

                <i class="fa fa-binoculars" aria-hidden="true"></i>

                <i class="fa fa-birthday-cake" aria-hidden="true"></i>

                <i class="fa fa-blind" aria-hidden="true"></i>

                <i class="fa fa-bluetooth" aria-hidden="true"></i>

                <i class="fa fa-bluetooth-b" aria-hidden="true"></i>

                <i class="fa fa-bolt" aria-hidden="true"></i>

                <i class="fa fa-bomb" aria-hidden="true"></i>

                <i class="fa fa-book" aria-hidden="true"></i>

                <i class="fa fa-bookmark" aria-hidden="true"></i>

                <i class="fa fa-bookmark-o" aria-hidden="true"></i>

                <i class="fa fa-braille" aria-hidden="true"></i>

                <i class="fa fa-briefcase" aria-hidden="true"></i>

                <i class="fa fa-bug" aria-hidden="true"></i>

                <i class="fa fa-building" aria-hidden="true"></i>

                <i class="fa fa-building-o" aria-hidden="true"></i>

                <i class="fa fa-bullhorn" aria-hidden="true"></i>

                <i class="fa fa-bullseye" aria-hidden="true"></i>

                <i class="fa fa-bus" aria-hidden="true"></i>

                <i class="fa fa-cab" aria-hidden="true"></i>

                <i class="fa fa-calculator" aria-hidden="true"></i>

                <i class="fa fa-calendar" aria-hidden="true"></i>

                <i class="fa fa-calendar-check-o" aria-hidden="true"></i>

                <i class="fa fa-calendar-minus-o" aria-hidden="true"></i>

                <i class="fa fa-calendar-o" aria-hidden="true"></i>

                <i class="fa fa-calendar-plus-o" aria-hidden="true"></i>

                <i class="fa fa-calendar-times-o" aria-hidden="true"></i>

                <i class="fa fa-camera" aria-hidden="true"></i>

                <i class="fa fa-camera-retro" aria-hidden="true"></i>

                <i class="fa fa-car" aria-hidden="true"></i>

                <i class="fa fa-caret-square-o-down" aria-hidden="true"></i>

                <i class="fa fa-caret-square-o-left" aria-hidden="true"></i>

                <i class="fa fa-caret-square-o-right" aria-hidden="true"></i>

                <i class="fa fa-caret-square-o-up" aria-hidden="true"></i>

                <i class="fa fa-cart-arrow-down" aria-hidden="true"></i>

                <i class="fa fa-cart-plus" aria-hidden="true"></i>

                <i class="fa fa-cc" aria-hidden="true"></i>

                <i class="fa fa-certificate" aria-hidden="true"></i>

                <i class="fa fa-check" aria-hidden="true"></i>

                <i class="fa fa-check-circle" aria-hidden="true"></i>

                <i class="fa fa-check-circle-o" aria-hidden="true"></i>

                <i class="fa fa-check-square" aria-hidden="true"></i>

                <i class="fa fa-check-square-o" aria-hidden="true"></i>

                <i class="fa fa-child" aria-hidden="true"></i>

                <i class="fa fa-circle" aria-hidden="true"></i>

                <i class="fa fa-circle-o" aria-hidden="true"></i>

                <i class="fa fa-circle-o-notch" aria-hidden="true"></i>

                <i class="fa fa-circle-thin" aria-hidden="true"></i>

                <i class="fa fa-clock-o" aria-hidden="true"></i>

                <i class="fa fa-clone" aria-hidden="true"></i>

                <i class="fa fa-close" aria-hidden="true"></i>

                <i class="fa fa-cloud" aria-hidden="true"></i>

                <i class="fa fa-cloud-download" aria-hidden="true"></i>

                <i class="fa fa-cloud-upload" aria-hidden="true"></i>

                <i class="fa fa-code" aria-hidden="true"></i>

                <i class="fa fa-code-fork" aria-hidden="true"></i>

                <i class="fa fa-coffee" aria-hidden="true"></i>

                <i class="fa fa-cog" aria-hidden="true"></i>

                <i class="fa fa-cogs" aria-hidden="true"></i>

                <i class="fa fa-comment" aria-hidden="true"></i>

                <i class="fa fa-comment-o" aria-hidden="true"></i>

                <i class="fa fa-commenting" aria-hidden="true"></i>

                <i class="fa fa-commenting-o" aria-hidden="true"></i>

                <i class="fa fa-comments" aria-hidden="true"></i>

                <i class="fa fa-comments-o" aria-hidden="true"></i>

                <i class="fa fa-compass" aria-hidden="true"></i>

                <i class="fa fa-copyright" aria-hidden="true"></i>

                <i class="fa fa-creative-commons" aria-hidden="true"></i>

                <i class="fa fa-credit-card" aria-hidden="true"></i>

                <i class="fa fa-credit-card-alt" aria-hidden="true"></i>

                <i class="fa fa-crop" aria-hidden="true"></i>

                <i class="fa fa-crosshairs" aria-hidden="true"></i>

                <i class="fa fa-cube" aria-hidden="true"></i>

                <i class="fa fa-cubes" aria-hidden="true"></i>

                <i class="fa fa-cutlery" aria-hidden="true"></i>

                <i class="fa fa-dashboard" aria-hidden="true"></i>

                <i class="fa fa-database" aria-hidden="true"></i>

                <i class="fa fa-deaf" aria-hidden="true"></i>

                <i class="fa fa-deafness" aria-hidden="true"></i>

                <i class="fa fa-desktop" aria-hidden="true"></i>

                <i class="fa fa-diamond" aria-hidden="true"></i>

                <i class="fa fa-dot-circle-o" aria-hidden="true"></i>

                <i class="fa fa-download" aria-hidden="true"></i>

                <i class="fa fa-drivers-license" aria-hidden="true"></i>

                <i class="fa fa-drivers-license-o" aria-hidden="true"></i>

                <i class="fa fa-edit" aria-hidden="true"></i>

                <i class="fa fa-ellipsis-h" aria-hidden="true"></i>

                <i class="fa fa-ellipsis-v" aria-hidden="true"></i>

                <i class="fa fa-envelope" aria-hidden="true"></i>

                <i class="fa fa-envelope-o" aria-hidden="true"></i>

                <i class="fa fa-envelope-open" aria-hidden="true"></i>

                <i class="fa fa-envelope-open-o" aria-hidden="true"></i>

                <i class="fa fa-envelope-square" aria-hidden="true"></i>

                <i class="fa fa-eraser" aria-hidden="true"></i>

                <i class="fa fa-exchange" aria-hidden="true"></i>

                <i class="fa fa-exclamation" aria-hidden="true"></i>

                <i class="fa fa-exclamation-circle" aria-hidden="true"></i>

                <i class="fa fa-exclamation-triangle" aria-hidden="true"></i>

                <i class="fa fa-external-link" aria-hidden="true"></i>

                <i class="fa fa-external-link-square" aria-hidden="true"></i>

                <i class="fa fa-eye" aria-hidden="true"></i>

                <i class="fa fa-eye-slash" aria-hidden="true"></i>

                <i class="fa fa-eyedropper" aria-hidden="true"></i>

                <i class="fa fa-fax" aria-hidden="true"></i>

                <i class="fa fa-feed" aria-hidden="true"></i>

                <i class="fa fa-female" aria-hidden="true"></i>

                <i class="fa fa-fighter-jet" aria-hidden="true"></i>

                <i class="fa fa-file-archive-o" aria-hidden="true"></i>

                <i class="fa fa-file-audio-o" aria-hidden="true"></i>

                <i class="fa fa-file-code-o" aria-hidden="true"></i>

                <i class="fa fa-file-excel-o" aria-hidden="true"></i>

                <i class="fa fa-file-image-o" aria-hidden="true"></i>

                <i class="fa fa-file-movie-o" aria-hidden="true"></i>

                <i class="fa fa-file-pdf-o" aria-hidden="true"></i>

                <i class="fa fa-file-photo-o" aria-hidden="true"></i>

                <i class="fa fa-file-picture-o" aria-hidden="true"></i>

                <i class="fa fa-file-powerpoint-o" aria-hidden="true"></i>

                <i class="fa fa-file-sound-o" aria-hidden="true"></i>

                <i class="fa fa-file-video-o" aria-hidden="true"></i>

                <i class="fa fa-file-word-o" aria-hidden="true"></i>

                <i class="fa fa-file-zip-o" aria-hidden="true"></i>

                <i class="fa fa-film" aria-hidden="true"></i>

                <i class="fa fa-filter" aria-hidden="true"></i>

                <i class="fa fa-fire" aria-hidden="true"></i>

                <i class="fa fa-fire-extinguisher" aria-hidden="true"></i>

                <i class="fa fa-flag" aria-hidden="true"></i>

                <i class="fa fa-flag-checkered" aria-hidden="true"></i>

                <i class="fa fa-flag-o" aria-hidden="true"></i>

                <i class="fa fa-flash" aria-hidden="true"></i>

                <i class="fa fa-flask" aria-hidden="true"></i>

                <i class="fa fa-folder" aria-hidden="true"></i>

                <i class="fa fa-folder-o" aria-hidden="true"></i>

                <i class="fa fa-folder-open" aria-hidden="true"></i>

                <i class="fa fa-folder-open-o" aria-hidden="true"></i>

                <i class="fa fa-frown-o" aria-hidden="true"></i>

                <i class="fa fa-futbol-o" aria-hidden="true"></i>

                <i class="fa fa-gamepad" aria-hidden="true"></i>

                <i class="fa fa-gavel" aria-hidden="true"></i>

                <i class="fa fa-gear" aria-hidden="true"></i>

                <i class="fa fa-gears" aria-hidden="true"></i>

                <i class="fa fa-gift" aria-hidden="true"></i>

                <i class="fa fa-glass" aria-hidden="true"></i>

                <i class="fa fa-globe" aria-hidden="true"></i>

                <i class="fa fa-graduation-cap" aria-hidden="true"></i>

                <i class="fa fa-group" aria-hidden="true"></i>

                <i class="fa fa-hand-grab-o" aria-hidden="true"></i>

                <i class="fa fa-hand-lizard-o" aria-hidden="true"></i>

                <i class="fa fa-hand-paper-o" aria-hidden="true"></i>

                <i class="fa fa-hand-peace-o" aria-hidden="true"></i>

                <i class="fa fa-hand-pointer-o" aria-hidden="true"></i>

                <i class="fa fa-hand-rock-o" aria-hidden="true"></i>

                <i class="fa fa-hand-scissors-o" aria-hidden="true"></i>

                <i class="fa fa-hand-spock-o" aria-hidden="true"></i>

                <i class="fa fa-hand-stop-o" aria-hidden="true"></i>

                <i class="fa fa-handshake-o" aria-hidden="true"></i>

                <i class="fa fa-hard-of-hearing" aria-hidden="true"></i>

                <i class="fa fa-hashtag" aria-hidden="true"></i>

                <i class="fa fa-hdd-o" aria-hidden="true"></i>

                <i class="fa fa-headphones" aria-hidden="true"></i>

                <i class="fa fa-heart" aria-hidden="true"></i>

                <i class="fa fa-heart-o" aria-hidden="true"></i>

                <i class="fa fa-heartbeat" aria-hidden="true"></i>

                <i class="fa fa-history" aria-hidden="true"></i>

                <i class="fa fa-home" aria-hidden="true"></i>

                <i class="fa fa-hotel" aria-hidden="true"></i>

                <i class="fa fa-hourglass" aria-hidden="true"></i>

                <i class="fa fa-hourglass-1" aria-hidden="true"></i>

                <i class="fa fa-hourglass-2" aria-hidden="true"></i>

                <i class="fa fa-hourglass-3" aria-hidden="true"></i>

                <i class="fa fa-hourglass-end" aria-hidden="true"></i>

                <i class="fa fa-hourglass-half" aria-hidden="true"></i>

                <i class="fa fa-hourglass-o" aria-hidden="true"></i>

                <i class="fa fa-hourglass-start" aria-hidden="true"></i>

                <i class="fa fa-i-cursor" aria-hidden="true"></i>

                <i class="fa fa-id-badge" aria-hidden="true"></i>

                <i class="fa fa-id-card" aria-hidden="true"></i>

                <i class="fa fa-id-card-o" aria-hidden="true"></i>

                <i class="fa fa-image" aria-hidden="true"></i>

                <i class="fa fa-inbox" aria-hidden="true"></i>

                <i class="fa fa-industry" aria-hidden="true"></i>

                <i class="fa fa-info" aria-hidden="true"></i>

                <i class="fa fa-info-circle" aria-hidden="true"></i>

                <i class="fa fa-institution" aria-hidden="true"></i>

                <i class="fa fa-key" aria-hidden="true"></i>

                <i class="fa fa-keyboard-o" aria-hidden="true"></i>

                <i class="fa fa-language" aria-hidden="true"></i>

                <i class="fa fa-laptop" aria-hidden="true"></i>

                <i class="fa fa-leaf" aria-hidden="true"></i>

                <i class="fa fa-legal" aria-hidden="true"></i>

                <i class="fa fa-lemon-o" aria-hidden="true"></i>

                <i class="fa fa-level-down" aria-hidden="true"></i>

                <i class="fa fa-level-up" aria-hidden="true"></i>

                <i class="fa fa-life-bouy" aria-hidden="true"></i>

                <i class="fa fa-life-buoy" aria-hidden="true"></i>

                <i class="fa fa-life-ring" aria-hidden="true"></i>

                <i class="fa fa-life-saver" aria-hidden="true"></i>

                <i class="fa fa-lightbulb-o" aria-hidden="true"></i>

                <i class="fa fa-line-chart" aria-hidden="true"></i>

                <i class="fa fa-location-arrow" aria-hidden="true"></i>

                <i class="fa fa-lock" aria-hidden="true"></i>

                <i class="fa fa-low-vision" aria-hidden="true"></i>

                <i class="fa fa-magic" aria-hidden="true"></i>

                <i class="fa fa-magnet" aria-hidden="true"></i>

                <i class="fa fa-mail-forward" aria-hidden="true"></i>

                <i class="fa fa-mail-reply" aria-hidden="true"></i>

                <i class="fa fa-mail-reply-all" aria-hidden="true"></i>

                <i class="fa fa-male" aria-hidden="true"></i>

                <i class="fa fa-map" aria-hidden="true"></i>

                <i class="fa fa-map-marker" aria-hidden="true"></i>

                <i class="fa fa-map-o" aria-hidden="true"></i>

                <i class="fa fa-map-pin" aria-hidden="true"></i>

                <i class="fa fa-map-signs" aria-hidden="true"></i>

                <i class="fa fa-meh-o" aria-hidden="true"></i>

                <i class="fa fa-microchip" aria-hidden="true"></i>

                <i class="fa fa-microphone" aria-hidden="true"></i>

                <i class="fa fa-microphone-slash" aria-hidden="true"></i>

                <i class="fa fa-minus" aria-hidden="true"></i>

                <i class="fa fa-minus-circle" aria-hidden="true"></i>

                <i class="fa fa-minus-square" aria-hidden="true"></i>

                <i class="fa fa-minus-square-o" aria-hidden="true"></i>

                <i class="fa fa-mobile" aria-hidden="true"></i>

                <i class="fa fa-mobile-phone" aria-hidden="true"></i>

                <i class="fa fa-money" aria-hidden="true"></i>

                <i class="fa fa-moon-o" aria-hidden="true"></i>

                <i class="fa fa-mortar-board" aria-hidden="true"></i>

                <i class="fa fa-motorcycle" aria-hidden="true"></i>

                <i class="fa fa-mouse-pointer" aria-hidden="true"></i>

                <i class="fa fa-music" aria-hidden="true"></i>

                <i class="fa fa-navicon" aria-hidden="true"></i>

                <i class="fa fa-newspaper-o" aria-hidden="true"></i>

                <i class="fa fa-object-group" aria-hidden="true"></i>

                <i class="fa fa-object-ungroup" aria-hidden="true"></i>

                <i class="fa fa-paint-brush" aria-hidden="true"></i>

                <i class="fa fa-paper-plane" aria-hidden="true"></i>

                <i class="fa fa-paper-plane-o" aria-hidden="true"></i>

                <i class="fa fa-paw" aria-hidden="true"></i>

                <i class="fa fa-pencil" aria-hidden="true"></i>

                <i class="fa fa-pencil-square" aria-hidden="true"></i>

                <i class="fa fa-pencil-square-o" aria-hidden="true"></i>

                <i class="fa fa-percent" aria-hidden="true"></i>

                <i class="fa fa-phone" aria-hidden="true"></i>

                <i class="fa fa-phone-square" aria-hidden="true"></i>

                <i class="fa fa-photo" aria-hidden="true"></i>

                <i class="fa fa-picture-o" aria-hidden="true"></i>

                <i class="fa fa-pie-chart" aria-hidden="true"></i>

                <i class="fa fa-plane" aria-hidden="true"></i>

                <i class="fa fa-plug" aria-hidden="true"></i>

                <i class="fa fa-plus" aria-hidden="true"></i>

                <i class="fa fa-plus-circle" aria-hidden="true"></i>

                <i class="fa fa-plus-square" aria-hidden="true"></i>

                <i class="fa fa-plus-square-o" aria-hidden="true"></i>

                <i class="fa fa-podcast" aria-hidden="true"></i>

                <i class="fa fa-power-off" aria-hidden="true"></i>

                <i class="fa fa-print" aria-hidden="true"></i>

                <i class="fa fa-puzzle-piece" aria-hidden="true"></i>

                <i class="fa fa-qrcode" aria-hidden="true"></i>

                <i class="fa fa-question" aria-hidden="true"></i>

                <i class="fa fa-question-circle" aria-hidden="true"></i>

                <i class="fa fa-question-circle-o" aria-hidden="true"></i>

                <i class="fa fa-quote-left" aria-hidden="true"></i>

                <i class="fa fa-quote-right" aria-hidden="true"></i>

                <i class="fa fa-random" aria-hidden="true"></i>

                <i class="fa fa-recycle" aria-hidden="true"></i>

                <i class="fa fa-refresh" aria-hidden="true"></i>

                <i class="fa fa-registered" aria-hidden="true"></i>

                <i class="fa fa-remove" aria-hidden="true"></i>

                <i class="fa fa-reorder" aria-hidden="true"></i>

                <i class="fa fa-reply" aria-hidden="true"></i>

                <i class="fa fa-reply-all" aria-hidden="true"></i>

                <i class="fa fa-retweet" aria-hidden="true"></i>

                <i class="fa fa-road" aria-hidden="true"></i>

                <i class="fa fa-rocket" aria-hidden="true"></i>

                <i class="fa fa-rss" aria-hidden="true"></i>

                <i class="fa fa-rss-square" aria-hidden="true"></i>

                <i class="fa fa-s15" aria-hidden="true"></i>

                <i class="fa fa-search" aria-hidden="true"></i>

                <i class="fa fa-search-minus" aria-hidden="true"></i>

                <i class="fa fa-search-plus" aria-hidden="true"></i>

                <i class="fa fa-send" aria-hidden="true"></i>

                <i class="fa fa-send-o" aria-hidden="true"></i>

                <i class="fa fa-server" aria-hidden="true"></i>

                <i class="fa fa-share" aria-hidden="true"></i>

                <i class="fa fa-share-alt" aria-hidden="true"></i>

                <i class="fa fa-share-alt-square" aria-hidden="true"></i>

                <i class="fa fa-share-square" aria-hidden="true"></i>

                <i class="fa fa-share-square-o" aria-hidden="true"></i>

                <i class="fa fa-shield" aria-hidden="true"></i>

                <i class="fa fa-ship" aria-hidden="true"></i>

                <i class="fa fa-shopping-bag" aria-hidden="true"></i>

                <i class="fa fa-shopping-basket" aria-hidden="true"></i>

                <i class="fa fa-shopping-cart" aria-hidden="true"></i>

                <i class="fa fa-shower" aria-hidden="true"></i>

                <i class="fa fa-sign-in" aria-hidden="true"></i>

                <i class="fa fa-sign-language" aria-hidden="true"></i>

                <i class="fa fa-sign-out" aria-hidden="true"></i>

                <i class="fa fa-signal" aria-hidden="true"></i>

                <i class="fa fa-signing" aria-hidden="true"></i>

                <i class="fa fa-sitemap" aria-hidden="true"></i>

                <i class="fa fa-sliders" aria-hidden="true"></i>

                <i class="fa fa-smile-o" aria-hidden="true"></i>

                <i class="fa fa-snowflake-o" aria-hidden="true"></i>

                <i class="fa fa-soccer-ball-o" aria-hidden="true"></i>

                <i class="fa fa-sort" aria-hidden="true"></i>

                <i class="fa fa-sort-alpha-asc" aria-hidden="true"></i>

                <i class="fa fa-sort-alpha-desc" aria-hidden="true"></i>

                <i class="fa fa-sort-amount-asc" aria-hidden="true"></i>

                <i class="fa fa-sort-amount-desc" aria-hidden="true"></i>

                <i class="fa fa-sort-asc" aria-hidden="true"></i>

                <i class="fa fa-sort-desc" aria-hidden="true"></i>

                <i class="fa fa-sort-down" aria-hidden="true"></i>

                <i class="fa fa-sort-numeric-asc" aria-hidden="true"></i>

                <i class="fa fa-sort-numeric-desc" aria-hidden="true"></i>

                <i class="fa fa-sort-up" aria-hidden="true"></i>

                <i class="fa fa-space-shuttle" aria-hidden="true"></i>

                <i class="fa fa-spinner" aria-hidden="true"></i>

                <i class="fa fa-spoon" aria-hidden="true"></i>

                <i class="fa fa-square" aria-hidden="true"></i>

                <i class="fa fa-square-o" aria-hidden="true"></i>

                <i class="fa fa-star" aria-hidden="true"></i>

                <i class="fa fa-star-half" aria-hidden="true"></i>

                <i class="fa fa-star-half-empty" aria-hidden="true"></i>

                <i class="fa fa-star-half-full" aria-hidden="true"></i>

                <i class="fa fa-star-half-o" aria-hidden="true"></i>

                <i class="fa fa-star-o" aria-hidden="true"></i>

                <i class="fa fa-sticky-note" aria-hidden="true"></i>

                <i class="fa fa-sticky-note-o" aria-hidden="true"></i>

                <i class="fa fa-street-view" aria-hidden="true"></i>

                <i class="fa fa-suitcase" aria-hidden="true"></i>

                <i class="fa fa-sun-o" aria-hidden="true"></i>

                <i class="fa fa-support" aria-hidden="true"></i>

                <i class="fa fa-tablet" aria-hidden="true"></i>

                <i class="fa fa-tachometer" aria-hidden="true"></i>

                <i class="fa fa-tag" aria-hidden="true"></i>

                <i class="fa fa-tags" aria-hidden="true"></i>

                <i class="fa fa-tasks" aria-hidden="true"></i>

                <i class="fa fa-taxi" aria-hidden="true"></i>

                <i class="fa fa-television" aria-hidden="true"></i>

                <i class="fa fa-terminal" aria-hidden="true"></i>

                <i class="fa fa-thermometer" aria-hidden="true"></i>

                <i class="fa fa-thermometer-0" aria-hidden="true"></i>

                <i class="fa fa-thermometer-1" aria-hidden="true"></i>

                <i class="fa fa-thermometer-2" aria-hidden="true"></i>

                <i class="fa fa-thermometer-3" aria-hidden="true"></i>

                <i class="fa fa-thermometer-4" aria-hidden="true"></i>

                <i class="fa fa-thermometer-empty" aria-hidden="true"></i>

                <i class="fa fa-thermometer-full" aria-hidden="true"></i>

                <i class="fa fa-thermometer-half" aria-hidden="true"></i>

                <i class="fa fa-thermometer-quarter" aria-hidden="true"></i>

                <i class="fa fa-thermometer-three-quarters" aria-hidden="true"></i>

                <i class="fa fa-thumb-tack" aria-hidden="true"></i>

                <i class="fa fa-thumbs-down" aria-hidden="true"></i>

                <i class="fa fa-thumbs-o-down" aria-hidden="true"></i>

                <i class="fa fa-thumbs-o-up" aria-hidden="true"></i>

                <i class="fa fa-thumbs-up" aria-hidden="true"></i>

                <i class="fa fa-ticket" aria-hidden="true"></i>

                <i class="fa fa-times" aria-hidden="true"></i>

                <i class="fa fa-times-circle" aria-hidden="true"></i>

                <i class="fa fa-times-circle-o" aria-hidden="true"></i>

                <i class="fa fa-times-rectangle" aria-hidden="true"></i>

                <i class="fa fa-times-rectangle-o" aria-hidden="true"></i>

                <i class="fa fa-tint" aria-hidden="true"></i>

                <i class="fa fa-toggle-down" aria-hidden="true"></i>

                <i class="fa fa-toggle-left" aria-hidden="true"></i>

                <i class="fa fa-toggle-off" aria-hidden="true"></i>

                <i class="fa fa-toggle-on" aria-hidden="true"></i>

                <i class="fa fa-toggle-right" aria-hidden="true"></i>

                <i class="fa fa-toggle-up" aria-hidden="true"></i>

                <i class="fa fa-trademark" aria-hidden="true"></i>

                <i class="fa fa-trash" aria-hidden="true"></i>

                <i class="fa fa-trash-o" aria-hidden="true"></i>

                <i class="fa fa-tree" aria-hidden="true"></i>

                <i class="fa fa-trophy" aria-hidden="true"></i>

                <i class="fa fa-truck" aria-hidden="true"></i>

                <i class="fa fa-tty" aria-hidden="true"></i>

                <i class="fa fa-tv" aria-hidden="true"></i>

                <i class="fa fa-umbrella" aria-hidden="true"></i>

                <i class="fa fa-universal-access" aria-hidden="true"></i>

                <i class="fa fa-university" aria-hidden="true"></i>

                <i class="fa fa-unlock" aria-hidden="true"></i>

                <i class="fa fa-unlock-alt" aria-hidden="true"></i>

                <i class="fa fa-unsorted" aria-hidden="true"></i>

                <i class="fa fa-upload" aria-hidden="true"></i>

                <i class="fa fa-user" aria-hidden="true"></i>

                <i class="fa fa-user-circle" aria-hidden="true"></i>

                <i class="fa fa-user-circle-o" aria-hidden="true"></i>

                <i class="fa fa-user-o" aria-hidden="true"></i>

                <i class="fa fa-user-plus" aria-hidden="true"></i>

                <i class="fa fa-user-secret" aria-hidden="true"></i>

                <i class="fa fa-user-times" aria-hidden="true"></i>

                <i class="fa fa-users" aria-hidden="true"></i>

                <i class="fa fa-vcard" aria-hidden="true"></i>

                <i class="fa fa-vcard-o" aria-hidden="true"></i>

                <i class="fa fa-video-camera" aria-hidden="true"></i>

                <i class="fa fa-volume-control-phone" aria-hidden="true"></i>

                <i class="fa fa-volume-down" aria-hidden="true"></i>

                <i class="fa fa-volume-off" aria-hidden="true"></i>

                <i class="fa fa-volume-up" aria-hidden="true"></i>

                <i class="fa fa-warning" aria-hidden="true"></i>

                <i class="fa fa-wheelchair" aria-hidden="true"></i>

                <i class="fa fa-wheelchair-alt" aria-hidden="true"></i>

                <i class="fa fa-wifi" aria-hidden="true"></i>

                <i class="fa fa-window-close" aria-hidden="true"></i>

                <i class="fa fa-window-close-o" aria-hidden="true"></i>

                <i class="fa fa-window-maximize" aria-hidden="true"></i>

                <i class="fa fa-window-minimize" aria-hidden="true"></i>

                <i class="fa fa-window-restore" aria-hidden="true"></i>

                <i class="fa fa-wrench" aria-hidden="true"></i>
              </div>
            </div>
          </div>
        </el-form-item>

        <el-form-item label="菜单状态:" prop="visible">
          <el-radio-group v-model="form.visible">
            <el-radio label="0">正常</el-radio>
            <el-radio label="1">隐藏</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer" v-if="!isDetail">
        <el-button class="" @click="open = false">取消</el-button>
        <el-button class="" type="primary" @click="submitForm('form')">保存</el-button>
      </div>
    </el-dialog>

    <!-- 新增，编辑弹框 -->
    <div class="dialog">
      <Tree width="40%" v-if="openTree" ref="treeDialog"></Tree>
    </div>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import Tree from "./tree";
export default {
  //import引入的组件需要注入到对象中才能使用
  components: { Tree },
  props: ["title", "width", "isDetail"],
  inject: ['getData'],
  data() {
    //这里存放数据
    return {
      // 是否显示弹出层
      open: false,
      form: {
        parentId: "0",
        menuType: "",
        menuName: "",
        url: "",
        target: "menuItem",
        perms: "",
        orderNum: "",
        icon: "",
        visible: "0",
        parentMenu: "主目录",
        menuId: "",
      },
      rules: {
        menuType: [{ required: true, message: "菜单类型不能为空", trigger: "change" }],
        menuName: [{ required: true, message: "菜单名称不能为空", trigger: "blur" }],
        orderNum: [{ required: true, message: "显示排序不能为空", trigger: "blur" }],
      },

      // 是否显示图标
      isShowIcon: false,

      // 是否显示树
      openTree: false,

      // 判断是新增还是编辑
      status: '',
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    // 窗口初始化方法，nextTick方法可以添加逻辑，如打开窗口时查询数据填充
    init(tableRadio, status) {
      this.open = true;
      this.status = status;
      this.$nextTick(() => {
        // 表单重置
        this.$refs["form"].resetFields();
        if (tableRadio) {
          this.$http({
            url: this.$http.adornUrl(`/system/menu/add/${tableRadio.menuId}`),
            method: "get",
            params: this.$http.adornParams({})
          }).then((res) => {
            if (res.data.menu) {
              let menu = res.data.menu;
              this.form.parentMenu = menu.menuName;
              this.form.parentId = menu.menuId;
            }
          });
        }
      });
    },

    edit(data, status) {
      this.open = true;
      this.status = status;
      this.$nextTick(() => {
        // 表单重置
        this.$refs["form"].resetFields();
        if (data) {
          this.$http({
            url: this.$http.adornUrl(`/system/menu/edit/${data.menuId}`),
            method: "get",
            params: this.$http.adornParams({})
          }).then((res) => {
            if (res.data.menu) {
              let menu = res.data.menu;
              this.form.parentMenu = menu.parentName ? menu.parentName : '无';
              this.form.parentId = menu.parentId;
              this.form.menuId = menu.menuId;
              this.form.menuType = menu.menuType;
              this.form.menuName = menu.menuName;
              this.form.url = menu.url;
              this.form.target = menu.target;
              this.form.perms = menu.perms;
              this.form.orderNum = menu.orderNum;
              this.form.icon = menu.icon;
              this.form.visible = menu.visible;

            }
          });
        }
      });
    },
    // 保存
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let params = {
            parentId: this.form.parentId,
            menuType: this.form.menuType,
            menuName: this.form.menuName,
            url: this.form.url,
            target: this.form.target,
            perms: this.form.perms,
            orderNum: this.form.orderNum,
            icon: this.form.icon,
            visible: this.form.visible,
          }
          if (this.status == 'edit') {
            params.menuId = this.form.menuId;
          }
          this.$http({
            url: this.$http.adornUrl(`/system/menu/${this.status}`),
            method: "post",
            params: this.$http.adornParams(params)
          }).then((res) => {
            if (res.data.code == 0) {
              this.$message({
                message: res.data.msg,
                type: "success"
              })
              setTimeout(() => {
                this.open = false;
                this.$parent.openDialog = false;
                this.getData();
              }, 1000);
            } else {
              this.$message({
                message: res.data.msg,
                type: "error"
              })
            }
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    getIcon(e) {
      this.form.icon = e.target.className;
      this.isShowIcon = false;
    },
    // 弹出树形框
    treeDialogFun() {
      this.openTree = true;
      this.$nextTick(() => {
        this.$refs.treeDialog.init(null);
      });
    }
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() { },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() { },
  beforeCreate() { }, //生命周期 - 创建之前
  beforeMount() { }, //生命周期 - 挂载之前
  beforeUpdate() { }, //生命周期 - 更新之前
  updated() { }, //生命周期 - 更新之后
  beforeDestroy() { }, //生命周期 - 销毁之前
  destroyed() { }, //生命周期 - 销毁完成
  activated() { }, //如果页面有keep-alive缓存功能，这个函数会触发
};
</script>
<style scoped>
/* @import url(); 引入公共css类 */
/* .dialog >>> .el-dialog {
  height: v-bind(height) !important;
} */
.dialog>>>.el-dialog {
  max-height: 77%;
}

#form {
  padding: 0 70px;
}

#form>>>.el-form-item__label {
  width: 30% !important;
}

.el-form-item {
  width: 100%;
  align-items: flex-start !important;
}

#form>>>.el-form-item__content {
  margin-left: 10px !important;
  width: 90% !important;
}

.ico-list .fa {
  margin: 5px;
  padding: 5px;
  cursor: pointer;
  font-size: 18px;
  width: 28px;
  border-radius: 3px;
}

.ico-list .fa:hover {
  background-color: #1d9d74;
  color: #ffffff;
}
</style>
