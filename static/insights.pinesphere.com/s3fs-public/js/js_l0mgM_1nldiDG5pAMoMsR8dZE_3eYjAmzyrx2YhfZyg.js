(function($,drupalSettings){'use strict';Drupal.behaviors.lang_dropdown={attach:function(context,settings){settings=settings||drupalSettings;if(settings.lang_dropdown){$('select.lang-dropdown-select-element').each(function(){var $dropdown=$(this);var key=$dropdown.data('lang-dropdown-id');var ldSettings=settings.lang_dropdown[key];if(ldSettings){var flags=ldSettings.languageicons;if(flags){$.each(flags,function(index,value){var option=$dropdown.find('option[value="'+index+'"]');if(ldSettings.widget==='msdropdown'){option.attr('data-image',value);}
else if(ldSettings.widget==='ddslick'&&Boolean(ldSettings.showSelectedHTML)){option.attr('data-imagesrc',value);}});}
if(ldSettings.widget==='msdropdown'){try{$dropdown.msDropDown({visibleRows:ldSettings.visibleRows,roundedCorner:Boolean(ldSettings.roundedCorner),animStyle:ldSettings.animStyle,event:ldSettings.event,mainCSS:ldSettings.mainCSS});}
catch(e){if(console){console.log(e);}}}
else if(ldSettings.widget==='chosen'){$dropdown.chosen({disable_search:ldSettings.disable_search,no_results_text:ldSettings.no_results_text});}
else if(ldSettings.widget==='ddslick'){$.data(document.body,'ddslick'+key+'flag',0);$dropdown.ddslick({width:ldSettings.width,height:(ldSettings.height===0)?null:ldSettings.height,showSelectedHTML:Boolean(ldSettings.showSelectedHTML),imagePosition:ldSettings.imagePosition,onSelected:function(data,element){var i=jQuery.data(document.body,'ddslick'+key+'flag');if(i){$.data(document.body,'ddslick'+key+'flag',0);data.selectedItem.closest('form').submit()}
$.data(document.body,'ddslick'+key+'flag',1);}});}}});}
$('select.lang-dropdown-select-element').change(function(){$(this).closest('form').submit();});}};})(jQuery,drupalSettings);;
(function($,Drupal,drupalSettings){"use strict";Drupal.TBMegaMenu=Drupal.TBMegaMenu||{};Drupal.TBMegaMenu.oldWindowWidth=0;Drupal.TBMegaMenu.displayedMenuMobile=false;Drupal.TBMegaMenu.supportedScreens=[980];Drupal.TBMegaMenu.focusableElements='a:not([disabled]), button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), details:not([disabled]), [tabindex]:not([disabled]):not([tabindex="-1"])';Drupal.TBMegaMenu.menuResponsive=function(){var windowWidth=window.innerWidth?window.innerWidth:$(window).width();var navCollapse=$('.tb-megamenu').children('.nav-collapse');if(windowWidth<Drupal.TBMegaMenu.supportedScreens[0]){navCollapse.addClass('collapse');if(Drupal.TBMegaMenu.displayedMenuMobile){navCollapse.css({height:'auto',overflow:'visible'});}
else{navCollapse.css({height:0,overflow:'hidden'});}}
else{navCollapse.removeClass('collapse');if(navCollapse.height()<=0){navCollapse.css({height:'auto',overflow:'visible'});}}};Drupal.TBMegaMenu.focusNextPrevElement=function(direction){var $current=$(document.activeElement);if($current.length){var $focusable=$(Drupal.TBMegaMenu.focusableElements).filter(function(){var $this=$(this);return $this.closest('.tb-megamenu-subnav').length===0&&$this.is(':visible');})
var index=$focusable.index($current);if(index>-1){if(direction==='next'){var nextElement=$focusable[index+1]||$focusable[0];}
else{var nextElement=$focusable[index-1]||$focusable[0];}
nextElement.focus();}}}
Drupal.behaviors.tbMegaMenuAction={attach:function(context,settings){$('.tb-megamenu',context).once('tb-megamenu').each(function(){var navParent=document.querySelector('.tb-megamenu'),linkArray=new Array(),curPos=new Array(-1,-1,-1);$(this).find('.level-1').children('a, span').not('.mobile-only').each(function(i,toplink){linkArray[i]=new Array();linkArray[i][-1]=toplink;$(toplink).data({coordinate:[i,-1]});$(toplink).next().children().children().children('.mega-col-nav').each(function(j,column){if($(column).find(Drupal.TBMegaMenu.focusableElements).length>0){linkArray[i][j]=new Array();$(column).find(Drupal.TBMegaMenu.focusableElements).each(function(k,sublink){linkArray[i][j][k]=sublink;$(sublink).data({coordinate:[i,j,k]});});}});});$(this).find(Drupal.TBMegaMenu.focusableElements).focus(function(){curPos=$(this).data('coordinate');});function keydownEvent(k){switch(k.keyCode){case 9:k.preventDefault();nav_tab(k);break;case 13:nav_open_link();break;case 27:nav_esc();break;case 37:k.preventDefault();nav_left();break;case 38:k.preventDefault();nav_up();break;case 39:k.preventDefault();nav_right();break;case 40:k.preventDefault();nav_down();break;case 36:nav_home();break;case 35:nav_end();break;default:}}
function nav_tab(k){if(nav_is_toplink()){if(k.shiftKey){nav_prev_toplink();}
else{nav_next_toplink();}}
else{if(k.shiftKey){nav_up();}
else{nav_down();}}}
function nav_open_link(){linkArray[curPos[0]][curPos[1]][curPos[2]].click();}
function nav_esc(){nav_close_megamenu();}
function nav_left(){if(nav_is_toplink()){nav_prev_toplink();}
else{nav_prev_column();}}
function nav_right(){if(nav_is_toplink()){nav_next_toplink();}
else{nav_next_column();}}
function nav_up(){if(nav_is_toplink()){nav_prev_toplink();}
else{if(linkArray[curPos[0]][curPos[1]][curPos[2]-1]){if($(linkArray[curPos[0]][curPos[1]][curPos[2]-1]).is(':visible')){linkArray[curPos[0]][curPos[1]][curPos[2]-1].focus();}
else{curPos=[curPos[0],curPos[1],curPos[2]-1];nav_up();}}
else{nav_prev_column();}}}
function nav_down(){if(nav_is_toplink()){nav_next_column();}
else{if(linkArray[curPos[0]][curPos[1]][curPos[2]+1]){linkArray[curPos[0]][curPos[1]][curPos[2]+1].focus();}
else{nav_next_column();}}}
function nav_home(){if(nav_is_toplink()){linkArray[0][-1].focus();}
else{linkArray[curPos[0]][0][0].focus();}}
function nav_end(){if(nav_is_toplink()){linkArray.slice(-1)[0][-1].focus();}
else{linkArray[curPos[0]].slice(-1)[0].slice(-1)[0].focus();}}
function nav_is_toplink(){return(curPos[1]<0);}
function nav_close_megamenu(){$('.tb-megamenu .open').removeClass('open');ariaCheck();}
function nav_next_toplink(){if(linkArray[curPos[0]+1]){linkArray[curPos[0]+1][-1].focus();}
else{nav_close_megamenu();Drupal.TBMegaMenu.focusNextPrevElement('next');}}
function nav_prev_toplink(){if(linkArray[curPos[0]-1]){linkArray[curPos[0]-1][-1].focus();}
else{Drupal.TBMegaMenu.focusNextPrevElement('prev');}}
function nav_prev_column(){if(linkArray[curPos[0]][curPos[1]-1][0]){linkArray[curPos[0]][curPos[1]-1][0].focus();}
else{nav_parent_toplink();}}
function nav_next_column(){if(linkArray[curPos[0]][curPos[1]+1]){linkArray[curPos[0]][curPos[1]+1][0].focus();}
else{nav_parent_toplink();}}
function nav_parent_toplink(){linkArray[curPos[0]][-1].focus();}
var ariaCheck=function(){$("li.tb-megamenu-item",this).each(function(){if($(this).is('.mega-group')){if(!$(this).parents().is('.open')){$(this).children().attr('aria-expanded','false');}
else if($(this).parents().is('.open')){$(this).children().attr('aria-expanded','true');}}
else if($(this).is('.dropdown')||$(this).is('.dropdown-submenu')){if(!$(this).is('.open')){$(this).children().attr('aria-expanded','false');}
else if($(this).is('.open')){$(this).children().attr('aria-expanded','true');}}
else{$(this).children().removeAttr('aria-expanded');}});};var showMenu=function($subMenu,mm_timeout){if($subMenu.hasClass('mega')){$subMenu.addClass('animating');clearTimeout($subMenu.data('animatingTimeout'));$subMenu.data('animatingTimeout',setTimeout(function(){$subMenu.removeClass('animating')},mm_timeout));clearTimeout($subMenu.data('hoverTimeout'));$subMenu.data('hoverTimeout',setTimeout(function(){$subMenu.addClass('open');ariaCheck();},100));}
else{clearTimeout($subMenu.data('hoverTimeout'));$subMenu.data('hoverTimeout',setTimeout(function(){$subMenu.addClass('open');ariaCheck();},100));}};var hideMenu=function($subMenu,mm_timeout){$subMenu.children('.dropdown-toggle').attr('aria-expanded','false');if($subMenu.hasClass('mega')){$subMenu.addClass('animating');clearTimeout($subMenu.data('animatingTimeout'));$subMenu.data('animatingTimeout',setTimeout(function(){$subMenu.removeClass('animating')},mm_timeout));clearTimeout($subMenu.data('hoverTimeout'));$subMenu.data('hoverTimeout',setTimeout(function(){$subMenu.removeClass('open');ariaCheck();},100));}
else{clearTimeout($subMenu.data('hoverTimeout'));$subMenu.data('hoverTimeout',setTimeout(function(){$subMenu.removeClass('open');ariaCheck();},100));}};$('.tb-megamenu-button',this).click(function(){if(parseInt($(this).parent().children('.nav-collapse').height())){$(this).parent().children('.nav-collapse').css({height:0,overflow:'hidden'});Drupal.TBMegaMenu.displayedMenuMobile=false;}
else{$(this).parent().children('.nav-collapse').css({height:'auto',overflow:'visible'});Drupal.TBMegaMenu.displayedMenuMobile=true;}});var isTouch=window.matchMedia('(pointer: coarse)').matches;if(!isTouch){var mm_duration=0;$('.tb-megamenu',context).each(function(){if($(this).data('duration')){mm_duration=$(this).data('duration');}});var mm_timeout=mm_duration?100+mm_duration:500;$('.nav > li, li.mega',context).bind('mouseenter',function(event){showMenu($(this),mm_timeout);});$('.nav > li > .dropdown-toggle, li.mega > .dropdown-toggle',context).bind('focus',function(event){var $this=$(this);var $subMenu=$this.closest('li');showMenu($subMenu,mm_timeout);$(document).bind('focusin',function(event){if($subMenu.has(event.target).length){return;}
$(document).unbind(event);hideMenu($subMenu,mm_timeout);});});$('.nav > li, li.mega',context).bind('mouseleave',function(event){hideMenu($(this),mm_timeout);});$('a, span').focus(function(event){if(!$(this).parent().hasClass('tb-megamenu-item')&&!$(this).parents('.tb-megamenu-block').length){nav_close_megamenu();}});$('.nav > li > a, li.mega > a').focus(function(event){var siblings=$(this).parents('.tb-megamenu-item').siblings();$.each(siblings,function(i,v){var cousins=$(v).find('.open');$.each(cousins,function(index,value){$(value).removeClass('open');ariaCheck($(this));});$(v).removeClass('open');ariaCheck();});if($(this).next(".tb-megamenu-submenu").length>0){if(!$(this).parent().hasClass("open")){$(this).parent().addClass("open");}}
if(!$(this).closest('.tb-megamenu-item.dropdown').hasClass('open')&&$(this).closest('.tb-megamenu-item.dropdown').find('.tb-megamenu-submenu').length>0){$(this).closest('.tb-megamenu-item.dropdown').addClass('open');ariaCheck();}
var parents=$(this).parents('.tb-megamenu-item.dropdown-submenu');$.each(parents,function(i,v){if(!$(v).hasClass('open')){$(v).addClass('open');ariaCheck();}});});}
var createTouchMenu=function(items){items.children("a, span").each(function(){var $item=$(this);var tbitem=$(this).parent();$item.click(function(event){if($item.hasClass("tb-megamenu-clicked")){var $uri=$item.attr("href");if($uri){window.location.href=$uri;}
else{$item.removeClass("tb-megamenu-clicked");hideMenu(tbitem,mm_timeout);}}
else{event.preventDefault();nav_close_megamenu();$(".tb-megamenu").find(".tb-megamenu-clicked").removeClass("tb-megamenu-clicked");$item.addClass("tb-megamenu-clicked");showMenu(tbitem,mm_timeout);}});});$(document).on('click',function(event){if($(event.target).closest('.tb-megamenu-nav').length===0){nav_close_megamenu();$(".tb-megamenu").find(".tb-megamenu-clicked").removeClass("tb-megamenu-clicked");};})};if(isTouch){createTouchMenu($(".tb-megamenu ul.nav li.mega",context).has(".dropdown-menu"));};$(window).on('load resize',function(){var windowWidth=window.innerWidth?window.innerWidth:$(window).width();if(windowWidth!=Drupal.TBMegaMenu.oldWindowWidth){Drupal.TBMegaMenu.oldWindowWidth=windowWidth;Drupal.TBMegaMenu.menuResponsive();if(windowWidth>=Drupal.TBMegaMenu.supportedScreens[0]){navParent.addEventListener('keydown',keydownEvent);}
else{navParent.removeEventListener('keydown',keydownEvent);}}});});}}})(jQuery,Drupal,drupalSettings);;
(($,Drupal,drupalSettings,once)=>{if(!Drupal.autocomplete){return;}
const autocomplete={};autocomplete.getSettings=(input,globalSettings)=>{globalSettings=globalSettings||drupalSettings||{};const settings={auto_submit:false,delay:0,min_length:1,selector:':submit',};const search=$(input).data('search-api-autocomplete-search');if(search&&globalSettings.search_api_autocomplete&&globalSettings.search_api_autocomplete[search]){$.extend(settings,globalSettings.search_api_autocomplete[search]);}
return settings;};Drupal.behaviors.searchApiAutocomplete={attach(context,settings){const s='.ui-autocomplete-input[data-search-api-autocomplete-search]';$(once('search-api-autocomplete',s,context)).each(function foreach(){const uiAutocomplete=$(this).data('ui-autocomplete');if(!uiAutocomplete){return;}
const $element=uiAutocomplete.menu.element;$element.data('search-api-autocomplete-input-id',this.id);$element.addClass('search-api-autocomplete-search');$element.attr('tabindex','-1');const elementSettings=autocomplete.getSettings(this,settings);if(elementSettings.delay){uiAutocomplete.options.delay=elementSettings.delay;}
if(elementSettings.min_length){uiAutocomplete.options.minLength=elementSettings.min_length;}
const oldSelect=uiAutocomplete.options.select;uiAutocomplete.options.select=function select(event,ui,...args){if(ui.item.url){if(event.keyCode===9){return false;}
window.location.href=ui.item.url;return false;}
const ret=oldSelect.apply(this,[event,ui,...args]);if(elementSettings.auto_submit&&elementSettings.selector){$(elementSettings.selector,this.form).trigger('click');}
return ret;};});},};Drupal.SearchApiAutocomplete=autocomplete;})(jQuery,Drupal,drupalSettings,once);;
