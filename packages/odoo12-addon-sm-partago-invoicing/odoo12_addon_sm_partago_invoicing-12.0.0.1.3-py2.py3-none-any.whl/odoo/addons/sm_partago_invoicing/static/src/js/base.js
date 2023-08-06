odoo.define('sm_partago_invoicing.base', function (require) {
  "use strict";

  var core = require('web.core');
  var ListController = require('web.ListController');
  var rpc = require('web.rpc');

  ListController.include({

    renderButtons: function ($node) {
      this._super.apply(this, arguments);
      if (this.$buttons) {
        let filter_button = this.$buttons.find('.oe_reservation_create_batch');
        filter_button && filter_button.click(this.proxy('filter_button'));
      }
    },

    filter_button: function () {
      //this.do_action('sm_partago.batch_reservation_compute_wizard');
      this.do_action({
        name: "Create batch compute",
        type: 'ir.actions.act_window',
        res_model: 'sm_partago_invoicing.sm_batch_reservation_compute.wizard',
        view_mode: 'form',
        view_type: 'form',
        views: [[false, 'form']],
         target: 'new',
      });
    }

  });
});