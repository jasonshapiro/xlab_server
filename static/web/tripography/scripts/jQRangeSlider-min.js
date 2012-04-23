/*
 jQRangeSlider Copyright (C) Guillaume Gautreau 2010, 2011
 A javascript slider selector that supports dates

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
var e=null;
(function(c){c.Ha("ui.rangeSlider",{options:{e:{min:0,max:100},B:{min:20,max:50},O:e,v:4,d:!0,u:"show",C:e,$:0,aa:400,Y:200},c:e,k:e,g:e,h:e,q:e,j:e,d:e,a:e,i:{min:!1,max:!1},ta:{min:!1,max:!1},M:0,r:0,F:0,Aa:function(){this.c=this.options.B;this.a={left:e,right:e,n:!0,o:!0};this.d={left:e,right:e};this.i={min:!1,max:!1};this.ta={min:!1,max:!1};this.g=c("<div class='ui-rangeSlider-handle  ui-rangeSlider-leftHandle' />").draggable({axis:"x",X:"parent",Z:c.f(this.T,this),stop:c.f(this.U,this)}).b("position",
"absolute");this.h=c("<div class='ui-rangeSlider-handle ui-rangeSlider-rightHandle' />").draggable({axis:"x",X:"parent",Z:c.f(this.T,this),stop:c.f(this.U,this)}).b("position","absolute");this.q=c("<div class='ui-rangeSlider-innerBar' />").b("position","absolute").b("top",0).b("left",0);this.j=c("<div class='ui-rangeSlider-container' />").b("position","absolute");this.k=c("<div class='ui-rangeSlider-bar' />").draggable({axis:"x",Z:c.f(this.ea,this),stop:c.f(this.fa,this),X:this.j}).b("position","absolute").bind("mousewheel",
c.f(this.ra,this));this.d.left=c("<div class='ui-rangeSlider-arrow ui-rangeSlider-leftArrow' />").b("position","absolute").b("left",0).bind("mousedown",c.f(this.na,this));this.d.right=c("<div class='ui-rangeSlider-arrow ui-rangeSlider-rightArrow' />").b("position","absolute").b("right",0).bind("mousedown",c.f(this.oa,this));c(document).bind("mouseup",c.f(this.pa,this));this.j.append(this.g).append(this.h).append(this.q).append(this.k);this.element.append(this.j).append(this.d.left).append(this.d.right).m("ui-rangeSlider").bind("mousewheel",
c.f(this.sa,this));this.element.b("position")!="absolute"&&this.element.b("position","relative");this.options.d?this.element.m("ui-rangeSlider-withArrows"):(this.d.left.b("display","none"),this.d.right.b("display","none"),this.element.m("ui-rangeSlider-noArrow"));this.options.u!="hide"?this.Q():this.H();c(window).Fa(c.f(this.la,this));this.Da(this.options);setTimeout(c.f(this.I,this),1);setTimeout(c.f(this.ka,this),1)},I:function(){this.j.b("width",this.element.width()-this.j.outerWidth(!0)+this.j.width());
this.q.b("width",this.j.width()-this.q.outerWidth(!0)+this.q.width())},ka:function(){this.t(this.options.B.min,this.options.B.max)},Ba:function(a,b){if(a=="defaultValues"){if(typeof b.min!="undefined"&&typeof b.max!="undefined"&&parseFloat(b.min)===b.min&&parseFloat(b.max)===b.max)this.options.B=b}else if(a=="wheelMode"&&(b=="zoom"||b=="scroll"||b===e))this.options.O=b;else if(a=="wheelSpeed"&&!isNaN(parseFloat(b))&&Math.abs(parseFloat(b))<=100)this.options.v=parseFloat(b);else if(a=="arrows"&&(b===
!0||b===!1)&&b!=this.options.d)b?(this.element.s("ui-rangeSlider-noArrow").m("ui-rangeSlider-withArrows"),this.d.left.b("display","block"),this.d.right.b("display","block")):(this.element.m("ui-rangeSlider-noArrow").s("ui-rangeSlider-withArrows"),this.d.left.b("display","none"),this.d.right.b("display","none")),this.options.d=b,this.I(),this.l();else if(a=="valueLabels"&&(b=="hide"||b=="show"||b=="change"))this.options.u=b,b!="hide"?this.Q():this.H();else if(a=="formatter"&&b!==e&&typeof b=="function")this.options.C=
b,this.l();else if(a=="bounds"&&typeof b.min!="undefined"&&typeof b.max!="undefined"&&parseFloat(b.min)===b.min&&parseFloat(b.max)===b.max&&b.min<b.max)this.options.e=b,this.t(this.c.min,this.c.max)},w:function(a){return(a-this.options.e.min)*(this.j.innerWidth()-1)/(this.options.e.max-this.options.e.min)},z:function(a){return a*(this.options.e.max-this.options.e.min)/(this.j.innerWidth()-1)+this.options.e.min},A:function(a,b){this.L(a,b);this.l();return this.c},p:function(a){this.element.Ga(a,{label:this.element,
t:this.t()})},l:function(){var a=this.w(this.c.min),b=this.w(this.c.max);this.J();this.k.b("left",a).b("width",b-a+this.k.width()-this.k.outerWidth(!0)+1)},J:function(){var a=this.w(this.c.min),b=this.w(this.c.max)-this.h.outerWidth(!0)+1;this.g.b("left",a);this.h.b("left",b);this.W()},ea:function(a,b){var c=b.position.left,d=c+this.k.outerWidth(!0)-1;this.L(this.z(c),this.z(d));this.J()},fa:function(){this.l();this.K()},qa:function(){var a=this.g;this.g=this.h;this.h=a;this.g.s("ui-rangeSlider-rightHandle").m("ui-rangeSlider-leftHandle");
this.h.m("ui-rangeSlider-rightHandle").s("ui-rangeSlider-leftHandle")},T:function(a,b){var c=this.c.min,d=this.c.max;if(b.ca[0]==this.g[0])c=this.z(b.position.left);else if(b.ca[0]==this.h[0])d=this.z(b.position.left-1+b.ca.outerWidth(!0));else return;if(c>d){this.qa();var f=c,c=d,d=f}this.A(c,d)},U:function(){this.l();this.K()},ga:function(a,b){this.p("valuesChanging");var c=!1;if(a&&!this.i.min)this.p("minValueChanging"),c=this.i.min=!0;if(b&&!this.i.max)this.p("maxValueChanging"),c=this.i.max=
!0;c&&this.ma()},K:function(){var a=this.M=Math.random();setTimeout(c.f(function(){this.ia(a)},this),200)},ia:function(a){if(this.M==a&&!this.k.ba("ui-draggable-dragging")&&!this.g.ba("ui-draggable-dragging")&&!this.h.ba("ui-draggable-dragging")){a=!1;if(this.i.min)this.i.min=!1,this.p("minValueChanged"),a=!0;if(this.i.max)this.i.max=!1,this.p("maxValueChanged"),a=!0;a&&this.p("valuesChanged");this.ja()}},Ca:function(a,b){this.L(a,b);this.J()},L:function(a,b){var c=this.c,d=Math.abs(b-a);if(d>=this.options.e.max-
this.options.e.min)this.c.min=this.options.e.min,this.c.max=this.options.e.max;else{var f={min:Math.min(b,a),max:Math.max(a,b)};if(f.min<this.options.e.min)f.min=this.options.e.min,f.max=f.min+d;else if(f.max>this.options.e.max)f.max=this.options.e.max,f.min=f.max-d;this.c=f}this.ga(c.min!=this.c.min,c.max!=this.c.max);this.K()},la:function(){this.I();this.l()},na:function(){this.r=Math.random();this.F=0;this.G(-1,this.r)},oa:function(){this.r=Math.random();this.F=0;this.G(1,this.r)},G:function(a,
b){b==this.r&&(this.N(a*(Math.min(Math.floor(this.F/5)+1,4)/4)),this.F++,setTimeout(c.f(function(){this.G(a,b)},this),50))},pa:function(){this.r=Math.random()},ra:function(a,b,c,d){if(this.options.O=="zoom")return this.da(-d),!1},sa:function(a,b,c,d){if(this.options.O=="scroll")return this.N(-d),!1},P:function(a,b){a===e&&(a=c("<div class='ui-rangeSlider-label'/>").m(b).b("position","absolute"),this.element.append(a),this.W());return a},R:function(a){a!==e&&(a.remove(),a=e);return a},Q:function(){this.a.left=
this.P(this.a.left,"ui-rangeSlider-leftLabel");this.a.right=this.P(this.a.right,"ui-rangeSlider-rightLabel");this.options.u=="change"?(this.a.left.b("display","none"),this.a.right.b("display","none"),this.a.n=!1,this.a.o=!1):(this.a.n=!0,this.a.o=!0,this.a.left.b("display","block"),this.a.right.b("display","block"),this.l())},H:function(){this.a.left=this.R(this.a.left);this.a.right=this.R(this.a.right)},V:function(a,b){var c=this.g.D().top-a.outerHeight(!0),d=a.offsetParent(),f=b-d.D().left;c-=d.D().top;
a.b("left",f).b("top",c)},W:function(){if(this.a.left!==e&&this.a.right!==e){this.a.left.text(this.S(this.c.min));this.a.right.text(this.S(this.c.max));var a=this.a.n?this.a.left.outerWidth(!0):0,b=this.a.o?this.a.right.outerWidth(!0):0,g=c(window).width()-b,d=Math.max(0,this.g.D().left+this.g.outerWidth(!0)/2-a/2),b=Math.min(g,this.h.D().left+this.h.outerWidth(!0)/2-b/2);d+a>=b&&(d=Math.max(0,d-(d+a-b)/2),b=Math.min(g,d+a),d=Math.max(0,b-a));this.a.n&&this.V(this.a.left,d);this.a.o&&this.V(this.a.right,
b)}},S:function(a){return typeof this.options.C!="undefined"&&this.options.C!==e?this.options.C(a):this.ha(a)},ha:function(a){return Math.round(a)},ma:function(){if(this.options.u=="change"&&!this.Ea){if(this.i.min&&!this.a.n)this.a.left.stop(!0,!0).wa(this.options.$),this.a.n=!0;if(this.i.max&&!this.a.o)this.a.o=!0,this.a.right.stop(!0,!0).wa(this.options.$)}},ja:function(){if(this.options.u=="change"&&this.a.left!==e&&this.a.right!==e)this.a.n=!1,this.a.o=!1,this.a.left.stop(!0,!0).ua(this.options.Y).xa(this.options.aa),
this.a.right.stop(!0,!0).ua(this.options.Y).xa(this.options.aa)},t:function(a,b){if(typeof a!="undefined"&&typeof b!="undefined")this.ya=!1,this.A(a,b),this.ya=!0;return this.c},min:function(a){return this.t(a,this.c.max).min},max:function(a){return this.t(this.c.min,a).max},da:function(a){var b=this.c.max-this.c.min;this.A(this.c.min+a*this.options.v*b/200,this.c.max-a*this.options.v*b/200)},Ia:function(a){this.da(-a)},scrollLeft:function(a){typeof a=="undefined"&&(a=1);this.N(-a)},N:function(a){typeof a==
"undefined"&&(a=1);var b=this.c.max-this.c.min;this.A(this.c.min+a*this.options.v*b/100,this.c.max+a*this.options.v*b/100)},va:function(){this.element.s("ui-rangeSlider-withArrows").s("ui-rangeSlider-noArrow");this.k.detach();this.g.detach();this.h.detach();this.q.detach();this.j.detach();this.d.left.detach();this.d.right.detach();this.element.s("ui-rangeSlider");this.H();delete this.options;c.za.prototype.va.apply(this,arguments)}})})(jQuery);
