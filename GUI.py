# this file has functions that create, populate and update the GUI
import wx

import gettext
import os
import pickle
import pandas as pd
import os.path
import Tkinter as tk
import Exp as exp
from ctypes import *
#import VMEC16 as vm
root = tk.Tk()
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        ### Gather Experiment names
        self.experiment_folder = "experiments/"
        if not(os.path.exists(self.experiment_folder)):
            os.makedirs(self.experiment_folder)
        if not(os.path.exists("data/")):
            os.makedirs("data/")
        self.experiment_list = os.listdir(self.experiment_folder)
        self.experiment_list_trimmed = []
        for i in self.experiment_list:
            self.experiment_list_trimmed.append(i.replace(".pickle", ""))
        if len(self.experiment_list_trimmed) == 0:
            self.experiment_list_trimmed = ["Empty"]
        ### Tasks
        self.task_list = ['None']
        self.participant_list = []
        self.participant_list_trimmed = []
        ### Current Experiment
        self.current_experiment = []
        self.current_experiment_name = ""
        self.highlit_experiment = ""
        ### Current Task
        self.highlit_task = ""
        self.highlit_task_num = 0
        self.min_angle_chosen = 40
        self.max_angle_chosen = 140
        self.num_trial_mult = 0
        self.num_target_chosen = 1
        self.num_trial_chosen = 1
        self.rotation_angle_chosen = 0
        self.lag_chosen = ""
        self.lag_chosen_err = ""
        self.num_target_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] 
        self.rotation_angle_list = ["0" , "30", "45", "60", "75"]
        ######################## VALID TEXT STUFF ##############################
        self.valid_lag_text = ""    
        self.valid_pause_text = ""
        self.valid_trial_num = 0
        
        ################### General Configuration Settings ###################
        self.general_cfg = {}
        ######################################################################
        self.Experiment_statictext = wx.StaticText(self, wx.ID_ANY, ("Experiments"))
        self.staticline_1 = wx.StaticLine(self, wx.ID_ANY, style=wx.EXPAND)
        self.exp_list_box = wx.ListBox(self, wx.ID_ANY, choices=self.experiment_list_trimmed)
        self.New_Button = wx.Button(self, wx.ID_ANY, ("New"))
        self.Delete_Button = wx.Button(self, wx.ID_ANY, ("Delete"))
        self.Load_Button = wx.Button(self, wx.ID_ANY, ("Load"))
        self.Save_Button = wx.Button(self, wx.ID_ANY, ("Save"))
        self.Run_Button = wx.Button(self, wx.ID_ANY, ("Run"))
        self.Task_statictext = wx.StaticText(self, wx.ID_ANY, ("Tasks"))
        
        self.participants_statictext = wx.StaticText(self, wx.ID_ANY, "Participants")
        self.participants_staticline = wx.StaticLine(self, wx.ID_ANY, style = wx.EXPAND)
        self.participants_list_box = wx.ListBox(self, wx.ID_ANY, choices=["Empty"])
        self.min_max_staticline = wx.StaticLine(self, wx.ID_ANY, style = wx.EXPAND)
        self.max_arrow_staticline = wx.StaticLine(self, wx.ID_ANY, style = wx.EXPAND)
        self.num_targets_staticline = wx.StaticLine(self, wx.ID_ANY, style = wx.EXPAND)
        self.num_trials_staticline = wx.StaticLine(self, wx.ID_ANY, style=wx.EXPAND)
        self.rotation_angle_staticline = wx.StaticLine(self, wx.ID_ANY, style=wx.EXPAND)
        self.rotation_change_staticline = wx.StaticLine(self, wx.ID_ANY, style=wx.EXPAND)
        self.target_distance_staticline = wx.StaticLine(self, wx.ID_ANY, style=wx.EXPAND)
        
        
        self.static_line2 = wx.StaticLine(self, wx.ID_ANY, style=wx.EXPAND)
        self.task_list_box = wx.ListBox(self, wx.ID_ANY, choices=self.task_list)
        self.Plus_Button = wx.Button(self, wx.ID_ANY, ("+"))
        self.Minus_Button = wx.Button(self, wx.ID_ANY, ("-"))
        self.radio_box_1 = wx.RadioBox(self, wx.ID_ANY, ("Task Type"), choices=[("Cursor"), ("No Cursor"), ("Pause"), ("Error Clamp")], majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.static_line_3 = wx.StaticLine(self, wx.ID_ANY, style=wx.EXPAND)
        self.min_angle_statictext = wx.StaticText(self, wx.ID_ANY, ("Minimum T-Angle"))        
        self.min_angle_CB = wx.Slider(self, wx.ID_ANY, minValue = 40, maxValue = 140, value = 40, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        
        self.max_angle_statictext = wx.StaticText(self, wx.ID_ANY, ("Maximum T-Angle"))
        self.max_angle_CB = wx.Slider(self, wx.ID_ANY, minValue = 40, maxValue = 140, value = 140, style=wx.SL_HORIZONTAL | wx.SL_LABELS)        
#        self.max_angle_CB = wx.ComboBox(self, wx.ID_ANY, choices=[("Cursor"), ("No Cursor"), ("Error Clamp")], style=wx.CB_DROPDOWN)       
        self.Move_Up_Button = wx.Button(self, wx.ID_ANY, (u"\u25b2"))
        self.Move_Down_Button = wx.Button(self, wx.ID_ANY, (u"\u25bc"))
        
        self.num_target_statictext = wx.StaticText(self, wx.ID_ANY, ("# Targets"))
        self.num_targ_CB = wx.ComboBox(self, wx.ID_ANY, value="3", choices=self.num_target_list, style=wx.CB_DROPDOWN)
        
        self.num_trials_statictext = wx.StaticText(self, wx.ID_ANY, ("# Trials"))
        self.num_trial_CB = wx.SpinCtrl(self, wx.ID_ANY, 'name', min=1, max=1000, initial=1, style=wx.SP_ARROW_KEYS | wx.SP_WRAP)
        
        self.Rotation_angle_statictext = wx.StaticText(self, wx.ID_ANY, (" Rotation Angle CW"))
        self.Rotation_angle_CB = wx.ComboBox(self, wx.ID_ANY, choices=self.rotation_angle_list, style=wx.CB_DROPDOWN)
        self.rot_change_statictext = wx.RadioBox(self, wx.ID_ANY, ("Rotation Change"), choices=[("Abrupt"), ("Gradual")], majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.lag_static_text = wx.StaticText(self, wx.ID_ANY, (" Lag (ms)"))
        self.lag_txt = wx.TextCtrl(self, wx.ID_ANY, ("0"))
        self.pause_static_text = wx.StaticText(self, wx.ID_ANY, ("Pause Time(s)"))
        self.pause_txt = wx.TextCtrl(self, wx.ID_ANY, ("0"))
        self.PM_static_text = wx.StaticText(self, wx.ID_ANY, (" Pause Message"))
        self.pause_message_txt = wx.TextCtrl(self, wx.ID_ANY, ("Text"))
        self.pause_check = wx.CheckBox(self, wx.ID_ANY, ("Space to continue"))
        self.target_distance_txt = wx.StaticText(self, wx.ID_ANY, ("Target Distance %"))
        self.target_distance_slider = wx.Slider(self, wx.ID_ANY, minValue = 50, maxValue = 100, style = wx.SL_HORIZONTAL | wx.SL_LABELS)
        
        # Hide pause stuff
        self.pause_static_text.Hide()
        self.pause_txt.Hide()
        self.PM_static_text.Hide()
        self.pause_message_txt.Hide()
        self.pause_check.Hide()
        

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.New_Press, self.New_Button)
        self.Bind(wx.EVT_BUTTON, self.Delete_Press, self.Delete_Button)
        self.Bind(wx.EVT_BUTTON, self.Load_Press, self.Load_Button)
        self.Bind(wx.EVT_BUTTON, self.Save_Press, self.Save_Button)
        self.Bind(wx.EVT_BUTTON, self.Run_Press, self.Run_Button)
        self.Bind(wx.EVT_BUTTON, self.Plus_Press, self.Plus_Button)
        self.Bind(wx.EVT_BUTTON, self.Minus_Press, self.Minus_Button)
        self.Bind(wx.EVT_RADIOBOX, self.Trial_Type_Press, self.radio_box_1)
        
        self.Bind(wx.EVT_SLIDER, self.min_angle_choose, self.min_angle_CB)       
        self.Bind(wx.EVT_SLIDER, self.max_angle_choose, self.max_angle_CB)
        self.Bind(wx.EVT_SLIDER, self.target_distance_choose, self.target_distance_slider)
        
        self.Bind(wx.EVT_BUTTON, self.Move_Up, self.Move_Up_Button)
        self.Bind(wx.EVT_BUTTON, self.Move_Down, self.Move_Down_Button)
        self.Bind(wx.EVT_COMBOBOX, self.num_target_choose, self.num_targ_CB)
        self.Bind(wx.EVT_SPINCTRL, self.num_trial_choose, self.num_trial_CB)
        self.Bind(wx.EVT_COMBOBOX, self.rot_angle_choose, self.Rotation_angle_CB)
        self.Bind(wx.EVT_RADIOBOX, self.Rot_Change_Press, self.rot_change_statictext)
        self.Bind(wx.EVT_TEXT, self.Lag_Enter, self.lag_txt)
        ### Pause events
        self.Bind(wx.EVT_TEXT, self.Pause_Enter, self.pause_txt)
        self.Bind(wx.EVT_TEXT, self.pause_message_make, self.pause_message_txt)
        self.Bind(wx.EVT_CHECKBOX, self.pause_check_press, self.pause_check)
        ### Experiment List Box Events
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.list_box_dclick, self.exp_list_box)
        self.Bind(wx.EVT_LISTBOX, self.list_box_click, self.exp_list_box)
        ### Task List Box Events
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.task_list_box_dclick, self.task_list_box)
        self.Bind(wx.EVT_LISTBOX, self.task_list_box_click, self.task_list_box)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(("Visuomotor"))
#        self.SetSize((798, 462)) ## Set size to this when Pause is selected
        self.SetSize((698, 500))
        self.Experiment_statictext.SetMinSize((70, 17))
        self.staticline_1.SetMinSize((175, 22))
        self.exp_list_box.SetMinSize((175, 150))
        self.exp_list_box.SetSelection(0)
        self.participants_list_box.SetMinSize((175,150))
        self.participants_list_box.SetSelection(0)
        self.participants_staticline.SetMinSize((175, 10))
        self.Run_Button.SetMinSize((175, 29))
        self.Save_Button.SetMinSize((85, 29))
        
        self.New_Button.SetMinSize((85, 29))
        self.Load_Button.SetMinSize((85, 29))

        self.Plus_Button.SetMinSize((85, 29))
        self.Minus_Button.SetMinSize((85, 29))        
        
        self.static_line2.SetMinSize((175, 22))
        self.min_max_staticline.SetMinSize((175, 22))
        self.static_line_3.SetMinSize((175, 22))
        self.max_arrow_staticline.SetMinSize((175, 22))  
        self.num_targets_staticline.SetMinSize((175, 22))
        self.num_trials_staticline.SetMinSize((175, 22))
        self.rotation_angle_staticline.SetMinSize((175, 22))
        self.rotation_change_staticline.SetMinSize((175, 22))
        
        self.task_list_box.SetMinSize((175, 332))
        self.task_list_box.SetSelection(0)
        self.radio_box_1.SetSelection(0)
        
        self.min_angle_CB.SetTickFreq(5, 1) #    
        self.max_angle_CB.SetTickFreq(5, 1) #
        
        self.Move_Up_Button.SetMinSize((30, 30))
        self.Move_Down_Button.SetMinSize((30, 30))
        self.num_targ_CB.SetSelection(-1)
#        self.num_trial_CB.SetSelection(-1)
        self.Rotation_angle_CB.SetSelection(-1)
        self.rot_change_statictext.SetSelection(0)
        ### Pause stuff
        self.pause_txt.SetMinSize((175,29))
        self.pause_message_txt.SetMinSize((175,29))
        # end wxGlade

    def __do_layout(self):
#        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.Experiment_statictext, 0, wx.EXPAND, 0)
        sizer_2.Add(self.staticline_1, 0, wx.BOTTOM, 5)
        sizer_2.Add(self.exp_list_box, 0, wx.RIGHT, 1)
        sizer_2.Add(self.participants_statictext, 0, wx.EXPAND, 0)
        sizer_2.Add(self.participants_staticline, 0, wx.BOTTOM, 5)
        sizer_2.Add(self.participants_list_box, 0, wx.RIGHT, 1)
        sizer_5.Add(self.New_Button, 0, wx.ALL, 2)
        sizer_5.Add(self.Delete_Button, 0, wx.ALL, 2)
        sizer_2.Add(sizer_5, 1, 0, 0)
        sizer_13.Add(self.Load_Button, 0, wx.ALL, 2)
        sizer_13.Add(self.Save_Button, 0, wx.ALL, 2)
        sizer_12.Add(sizer_13, 1, 0, 0)
        sizer_12.Add(self.Run_Button, 0, wx.ALL, 2)
        sizer_2.Add(sizer_12, 1, 0, 0)
        sizer_1.Add(sizer_2, 1, 0, 0)
        sizer_3.Add(self.Task_statictext, 0, wx.EXPAND, 0)
        sizer_3.Add(self.static_line2, 0, wx.BOTTOM, 5)
        sizer_3.Add(self.task_list_box, 0, wx.LEFT, 1)
        sizer_4.Add(self.Plus_Button, 0, wx.ALL, 2)
        sizer_4.Add(self.Minus_Button, 0, wx.ALL, 2)
        sizer_3.Add(sizer_4, 1, 0, 0)
        sizer_1.Add(sizer_3, 1, 0, 0)
        sizer_10.Add(self.radio_box_1, 0, 0, 0)
        sizer_10.Add(self.static_line_3, 0, wx.BOTTOM, 2)
        sizer_10.Add(self.min_angle_statictext, 0, 0, 0)
        sizer_10.Add(self.min_angle_CB, 0, wx.EXPAND, 0)
        sizer_10.Add(self.min_max_staticline, 0, wx.BOTTOM, 2)
        sizer_10.Add(self.max_angle_statictext, 0, 0, 0)
        sizer_10.Add(self.max_angle_CB, 0, wx.EXPAND, 0)
        sizer_10.Add(self.max_arrow_staticline, 0, wx.BOTTOM, 2)
        sizer_10.Add(self.target_distance_txt, 0, 0, 0)
        sizer_10.Add(self.target_distance_slider, 0, wx.EXPAND, 0)
        sizer_10.Add(self.target_distance_staticline, 0, wx.BOTTOM, 2)
        sizer_10.Add(self.pause_static_text, 0, 0, 0)
        sizer_10.Add(self.pause_txt, 0, 0, 0)
        sizer_10.Add(self.PM_static_text, 0, 0, 0)
        sizer_10.Add(self.pause_message_txt, 0, 0, 0)
        sizer_10.Add(self.pause_check, 0, 0, 0)
        sizer_10.Add(self.Move_Up_Button, 0, 0, 0)
        sizer_10.Add(self.Move_Down_Button, 0, 0, 0)
        sizer_8.Add(sizer_10, 1, 0, 0)
        sizer_9.Add(self.num_target_statictext, 0, wx.LEFT, 2)
        sizer_9.Add(self.num_targ_CB, 0, wx.LEFT, 2)
        sizer_9.Add(self.num_targets_staticline, 0, wx.BOTTOM, 2)
        sizer_9.Add(self.num_trials_statictext, 0, wx.LEFT, 2)
        sizer_9.Add(self.num_trial_CB, 0, wx.LEFT, 2)
        sizer_9.Add(self.num_trials_staticline, 0, wx.BOTTOM, 2)
        sizer_9.Add(self.Rotation_angle_statictext, 0, wx.LEFT, 2)
        sizer_9.Add(self.Rotation_angle_CB, 0, wx.LEFT, 2)
        sizer_9.Add(self.rotation_angle_staticline, 0, wx.BOTTOM, 2)
        sizer_9.Add(self.rot_change_statictext, 0, wx.LEFT, 2)
        sizer_9.Add(self.rotation_change_staticline, 0, wx.BOTTOM, 2)
        sizer_9.Add(self.lag_static_text, 0, wx.LEFT, 2)
        sizer_9.Add(self.lag_txt, 0, wx.LEFT, 2)
        sizer_8.Add(sizer_9, 1, 0, 0)
        sizer_1.Add(sizer_8, 1, 0, 0)
#        sizer_7.Add(self.lag_static_text, 0, 0, 0)
#        sizer_7.Add(self.lag_txt, 0, 0, 0)
        sizer_6.Add(sizer_7, 1, 0, 0)

        sizer_6.Add(sizer_11, 1, 0, 0)
        sizer_1.Add(sizer_6, 1, 0, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        
    def regular_experiment_show(self):
        ### Right most widgets ###
        self.num_target_statictext.Show()
        self.num_targ_CB.Show()
        self.num_targets_staticline.Show()
        self.num_trials_statictext.Show()
        self.num_trial_CB.Show()
        self.num_trials_staticline.Show()
        self.Rotation_angle_statictext.Show()     
        self.Rotation_angle_CB.Show()
        self.rotation_angle_staticline.Show() 
        self.rot_change_statictext.Show()
        self.rotation_change_staticline.Show()
        self.lag_static_text.Show()
        self.lag_txt.Show()
        ##### # # # # # # # # # # # # # # #
        self.min_angle_CB.Show()
        self.min_angle_statictext.Show()
        self.min_max_staticline.Show()
        self.max_angle_CB.Show()
        self.max_angle_statictext.Show()
        self.max_arrow_staticline.Show()
        ### Show ###
        self.pause_static_text.Hide()
        self.pause_txt.Hide()
        self.PM_static_text.Hide()
        self.pause_message_txt.Hide()
        self.pause_check.Hide()
        self.SetSize((698, 500))
    
    def pause_experiment_show(self):
        ### Right most widgets ###
        self.num_target_statictext.Hide()
        self.num_targ_CB.Hide()
        self.num_targets_staticline.Hide()
        self.num_trials_statictext.Hide()
        self.num_trial_CB.Hide()
        self.num_trials_staticline.Hide()
        self.Rotation_angle_statictext.Hide()        
        self.Rotation_angle_CB.Hide()
        self.rotation_angle_staticline.Hide()        
        self.rot_change_statictext.Hide()
        self.rotation_change_staticline.Hide()
        self.lag_static_text.Hide()
        self.lag_txt.Hide()
        ###
        self.min_angle_CB.Hide()
        self.min_angle_statictext.Hide()
        self.min_max_staticline.Hide()
        self.max_angle_CB.Hide()
        self.max_angle_statictext.Hide()
        self.max_arrow_staticline.Hide()
        ### Show ###
        self.pause_static_text.Show()
        self.pause_txt.Show()
        self.PM_static_text.Show()
        self.pause_message_txt.Show()
        self.pause_check.Show()
        self.SetSize((543, 500))
        
        
        
    def list_box_dclick(self, event):
        experimentFolder = self.highlit_experiment
        self.current_experiment_name = event.GetString()
        with open(self.experiment_folder + self.current_experiment_name + ".pickle", "rb") as f:
            self.current_experiment = pickle.load(f)
            del self.task_list[:]
        for i in range (0, len(self.current_experiment)):
            self.task_list.append(self.current_experiment[i]["task_name"])
        if len(self.task_list) == 0:
            self.task_list_box.Set(['Empty'])
        else:
            self.task_list_box.Set(self.task_list)
        #### REFRESH PARTICIPANT LIST #####
        if not(os.path.exists("data/" + experimentFolder)):
            os.makedirs("data/"+ experimentFolder)
        self.participant_list = os.listdir("data/" + self.current_experiment_name)
        for i in self.participant_list:
            self.participant_list_trimmed.append(i.replace(".csv", ""))
        if len(self.participant_list_trimmed) == 0:
            self.participant_list_trimmed = ["Empty"]
        self.participants_list_box.Set(self.participant_list_trimmed)
        del self.participant_list_trimmed[:]
        event.Skip()
    
    def list_box_click(self, event):
        self.highlit_experiment = event.GetString() ## The highlighted experiment
        event.Skip()
        
    def task_list_box_click(self, event):
        lag_conversion_factor = 37.2495/1000
        self.highlit_task = event.GetString()
        self.highlit_task_num = event.GetSelection()
        
        ### Trial number stuff
        self.valid_trial_num = self.current_experiment[self.highlit_task_num]['num_trials']
        if self.current_experiment[self.highlit_task_num]['num_targets'] > 2:
            self.num_trial_mult = self.current_experiment[self.highlit_task_num]['num_targets']
        elif self.current_experiment[self.highlit_task_num]['num_targets'] == 1:
            self.num_trial_mult = 3
        elif self.current_experiment[self.highlit_task_num]['num_targets'] == 2:
            self.num_trial_mult = 4
        ### Set Current Task Settings
        self.radio_box_1.SetSelection(exp.task_num(self.current_experiment[self.highlit_task_num]['trial_type'], True))
        self.num_trial_CB.SetValue(self.current_experiment[self.highlit_task_num]['num_trials'])
        self.num_targ_CB.SetStringSelection(str(self.current_experiment[self.highlit_task_num]['num_targets']))    
        # Show or hide Pause menu
        if self.current_experiment[self.highlit_task_num]['trial_type'] == "pause":
            self.pause_experiment_show()
            try:
                self.pause_txt.SetValue(str(self.current_experiment[self.highlit_task_num]['pausetime']))
                self.pause_message_txt.SetValue(self.current_experiment[self.highlit_task_num]['pause_instruction'])
            except:
                self.pause_txt.SetValue('0')
                self.pause_message_txt.SetValue('')
        else:
            self.regular_experiment_show()     
        
        self.min_angle_CB.SetValue(self.current_experiment[self.highlit_task_num]['min_angle'])                        
        self.max_angle_CB.SetValue(self.current_experiment[self.highlit_task_num]['max_angle'])
        try:
            self.lag_txt.SetValue(str(self.current_experiment[self.highlit_task_num]['lag_value']))
        except:
            self.lag_txt.SetValue("0")
        event.Skip()
    
    def task_list_box_dclick(self, event):
        dlg = wx.TextEntryDialog(self, 'Change Task Name', 'Rename')
        dlg.SetValue("Default")
        if dlg.ShowModal() == wx.ID_OK:
            self.current_experiment[self.highlit_task_num]["task_name"] = dlg.GetValue()
        del self.task_list[:]
        for i in range (0, len(self.current_experiment)):
            self.task_list.append(self.current_experiment[i]['task_name'])
        self.task_list_box.Set(self.task_list)
        dlg.Destroy()
        event.Skip()

    def New_Press(self, event):  # wxGlade: MyFrame.<event_handler>
        dlg = wx.TextEntryDialog(self, 'Enter Name', 'Create new experiment')
        dlg.SetValue("Default")
        
        if os.listdir(self.experiment_folder) == []:
            del self.experiment_list_trimmed[:]
        if dlg.ShowModal() == wx.ID_OK:
            new_experiment = []
            with open(self.experiment_folder + dlg.GetValue() + ".pickle", "wb") as f:
                pickle.dump(new_experiment, f)
            f.close()
            self.experiment_list_trimmed.append(dlg.GetValue())
            self.exp_list_box.Set(self.experiment_list_trimmed)
            self.exp_list_box.SetSelection(len(self.experiment_list_trimmed) - 1)
            self.current_experiment_name = dlg.GetValue()
            with open(self.experiment_folder + self.current_experiment_name + ".pickle", "rb") as f:
                self.current_experiment = pickle.load(f)
                del self.task_list[:]
            self.task_list_box.Set(["Empty"])
        dlg.Destroy()
        event.Skip()

    def Delete_Press(self, event):  # wxGlade: MyFrame.<event_handler>
        dlg = wx.MessageDialog(self, 'Confirm Deleting %s\n' % self.highlit_experiment,
                               'Delete Confirmation')
        if dlg.ShowModal() == wx.ID_OK:
            os.remove(self.experiment_folder + self.highlit_experiment + ".pickle")
            self.experiment_list_trimmed.remove(self.highlit_experiment)
            if os.listdir(self.experiment_folder) == []:
                self.experiment_list_trimmed = ["Empty"]
            self.exp_list_box.Set(self.experiment_list_trimmed)
        dlg.Destroy()
        event.Skip()

    def Load_Press(self, event):  # wxGlade: MyFrame.<event_handler>
        experimentFolder = self.highlit_experiment
        with open(self.experiment_folder+self.highlit_experiment+".pickle", "rb") as f:
            self.current_experiment = pickle.load(f)
            del self.task_list[:]
        for i in range (0, len(self.current_experiment)):
            self.task_list.append(exp.task_namer(self.current_experiment[i]["trial_type"], True))
        if len(self.task_list) == 0:
            self.task_list_box.Set(['Empty'])
        else:
            self.task_list_box.Set(self.task_list)
       #### REFRESH PARTICIPANT LIST #####
        if not(os.path.exists("data/" + experimentFolder)):
            os.makedirs("data/"+ experimentFolder)
        self.participant_list = os.listdir("data/" + self.current_experiment_name)
        for i in self.participant_list:
            self.participant_list_trimmed.append(i.replace(".csv", ""))
        if len(self.participant_list_trimmed) == 0:
            self.participant_list_trimmed = ["Empty"]
        self.participants_list_box.Set(self.participant_list_trimmed)
        del self.participant_list_trimmed[:]
        
        event.Skip()

    def Save_Press(self, event):
        dlg = wx.MessageDialog(self, "Save Experiment", style=wx.CENTRE|wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_OK:
            with open(self.experiment_folder+self.current_experiment_name+".pickle", "wb") as f:
                pickle.dump(self.current_experiment, f)
                f.close()
        dlg.Destroy()
        event.Skip()

    def Run_Press(self, event):  # wxGlade: MyFrame.<event_handle
        dlg = wx.TextEntryDialog(self, 'Enter name', 'Participant')
        dlg.SetValue("Default")
        experimentFolder = self.current_experiment_name
        if dlg.ShowModal() ==wx.ID_OK:  
            if (os.path.exists("data/" + experimentFolder + "/" + dlg.GetValue())):
                dlg2 = wx.MessageDialog(self, "Participant already exists!", style=wx.OK|wx.CENTRE|wx.ICON_WARNING)
                dlg2.ShowModal()
                dlg2.Destroy()
                return
            if not(os.path.exists("data/" + experimentFolder + "/" + dlg.GetValue())):
                os.makedirs("data/" + experimentFolder + "/" + dlg.GetValue())
            
            self.experiment_run = exp.run_experiment(True, self.current_experiment)
            self.experiment_run.to_csv(path_or_buf = "data/" + experimentFolder + "/" + dlg.GetValue() + "/" + dlg.GetValue() + ".csv")
        else:
            pass
        #### REFRESH PARTICIPANT LIST #####
        if not(os.path.exists("data/" + experimentFolder)):
            os.makedirs("data/"+ experimentFolder)
        self.participant_list = os.listdir("data/" + self.current_experiment_name)
        for i in self.participant_list:
            self.participant_list_trimmed.append(i.replace(".csv", ""))
        if len(self.participant_list_trimmed) == 0:
            self.participant_list_trimmed = ["Empty"]
        self.participants_list_box.Set(self.participant_list_trimmed)
        del self.participant_list_trimmed[:]
        dlg.Destroy()
        event.Skip()

    def Plus_Press(self, event):  # wxGlade: MyFrame.<event_handler>
        dlg = wx.TextEntryDialog(self, 'Enter Task Name', 'New Task')
        dlg.SetValue("Default")
        if dlg.ShowModal() == wx.ID_OK:
            with open("general_configurations.pickle", "rb") as f:
                new_task = pickle.load(f)
                self.current_experiment.append(new_task[0])
                self.highlit_task_num = len(self.current_experiment) - 1
                self.current_experiment[self.highlit_task_num]["task_name"] = dlg.GetValue()
                f.close()
            with open(self.experiment_folder + self.current_experiment_name + ".pickle", "wb") as f:
                pickle.dump(self.current_experiment, f)
                f.close()
            del self.task_list[:]
            for i in range (0, len(self.current_experiment)):
                self.task_list.append(self.current_experiment[i]['task_name'])
            self.task_list_box.Set(self.task_list)
            #### Set current highlit task to new task ####
            self.task_list_box.SetSelection(len(self.current_experiment) - 1)
            self.highlit_task = dlg.GetValue()
            self.highlit_task_num = len(self.current_experiment) - 1
            ### Set Current Task Settings
            self.radio_box_1.SetSelection(exp.task_num(self.current_experiment[self.highlit_task_num]['trial_type'], True))
            self.num_trial_CB.SetValue(self.current_experiment[self.highlit_task_num]['num_trials'])
            self.num_targ_CB.SetStringSelection(str(self.current_experiment[self.highlit_task_num]['num_targets']))    
            # Show or hide Pause menu
            if self.current_experiment[self.highlit_task_num]['trial_type'] == "pause":
                self.pause_experiment_show()
                try:
                    self.pause_txt.SetValue(str(self.current_experiment[self.highlit_task_num]['pausetime']))
                    self.pause_message_txt.SetValue(self.current_experiment[self.highlit_task_num]['pause_instruction'])
                except:
                    self.pause_txt.SetValue('0')
                    self.pause_message_txt.SetValue('')
            else:
                self.regular_experiment_show()     
            self.min_angle_CB.SetValue(self.current_experiment[self.highlit_task_num]['min_angle'])                        
            self.max_angle_CB.SetValue(self.current_experiment[self.highlit_task_num]['max_angle'])
            try:
                self.lag_txt.SetValue(str(self.current_experiment[self.highlit_task_num]['lag_value']))
            except:
                self.lag_txt.SetValue("0")
        else:
            pass
        dlg.Destroy()
        event.Skip()

    def Minus_Press(self, event):  # wxGlade: MyFrame.<event_handler>
        del self.current_experiment[self.highlit_task_num] # remove current task
        self.highlit_task_num = len(self.current_experiment) - 1
        with open(self.experiment_folder + self.current_experiment_name + ".pickle", "wb") as f:
            pickle.dump(self.current_experiment, f) #remove current task from file
            f.close()
        del self.task_list[:]
        # refresh task list
        for i in range (0, len(self.current_experiment)):
            self.task_list.append(exp.task_namer(self.current_experiment[i]["trial_type"], True))
        if len(self.task_list) == 0:
            self.task_list_box.Set(['None'])
        else:
            self.task_list_box.Set(self.task_list)
        
        event.Skip()

    def Trial_Type_Press(self, event):  # wxGlade: MyFrame.<event_handler>
        chosen_trial = event.GetString()
        if (chosen_trial == "Cursor"):
            self.current_experiment[self.highlit_task_num]["trial_type"] = "cursor"
            self.regular_experiment_show()
        elif(chosen_trial == "No Cursor"):
            self.current_experiment[self.highlit_task_num]["trial_type"] = "no_cursor"
            self.regular_experiment_show()
        elif(chosen_trial == "Pause"):
            self.current_experiment[self.highlit_task_num]["trial_type"] = "pause"
            self.pause_experiment_show()
        elif(chosen_trial == "Error Clamp"):
            self.current_experiment[self.highlit_task_num]["trial_type"] = "error_clamp"
            self.regular_experiment_show()
        with open(self.experiment_folder+self.current_experiment_name+".pickle", "wb") as f:
            pickle.dump(self.current_experiment, f)
            f.close()
        # refresh task list
        del self.task_list[:]
        for i in range (0, len(self.current_experiment)):
            self.task_list.append(self.current_experiment[i]['task_name'])
        if len(self.task_list) == 0:
            self.task_list_box.Set(['None'])
        else:
            self.task_list_box.Set(self.task_list)
        self.task_list_box.SetSelection(self.highlit_task_num)
        # save change

        event.Skip()

    def min_angle_choose(self, event):  # wxGlade: MyFrame.<event_handler>
        self.min_angle_chosen = exp.myRounder(event.GetInt(), 5) 
        if self.min_angle_chosen < self.max_angle_chosen:
            self.min_angle_CB.SetValue(self.min_angle_chosen)
        else:
            self.max_angle_chosen = self.min_angle_chosen
            self.min_angle_CB.SetValue(self.min_angle_chosen)
            self.max_angle_CB.SetValue(self.min_angle_chosen)
        self.current_experiment[self.highlit_task_num]['min_angle'] = self.min_angle_chosen
        self.current_experiment[self.highlit_task_num]['max_angle'] = self.max_angle_chosen      
        #save
        with open(self.experiment_folder+self.current_experiment_name+".pickle", "wb") as f:
            pickle.dump(self.current_experiment, f)
            f.close()
        event.Skip()
        
    def max_angle_choose(self, event):  # wxGlade: MyFrame.<event_handler>
        self.max_angle_chosen = exp.myRounder(event.GetInt(), 5)
        if self.max_angle_chosen > self.min_angle_chosen:
            self.max_angle_CB.SetValue(self.max_angle_chosen)
        else:
            self.min_angle_chosen = self.max_angle_chosen
            self.min_angle_CB.SetValue(self.min_angle_chosen)
            self.max_angle_CB.SetValue(self.min_angle_chosen)
        self.current_experiment[self.highlit_task_num]['min_angle'] = self.min_angle_chosen
        self.current_experiment[self.highlit_task_num]['max_angle'] = self.max_angle_chosen      
        #save        
        with open(self.experiment_folder+self.current_experiment_name+".pickle", "wb") as f:
            pickle.dump(self.current_experiment, f)
            f.close()
        event.Skip()

    def Move_Up(self, event):  # wxGlade: MyFrame.<event_handler>  
        if (self.highlit_task_num > 0):
            self.current_experiment[self.highlit_task_num], self.current_experiment[self.highlit_task_num - 1] = self.current_experiment[self.highlit_task_num - 1], self.current_experiment[self.highlit_task_num]
            self.highlit_task_num = self.highlit_task_num - 1
        with open(self.experiment_folder+self.current_experiment_name+".pickle", "wb") as f:
            pickle.dump(self.current_experiment, f)
            f.close()
        # refresh task list
        del self.task_list[:]
        for i in range (0, len(self.current_experiment)):
            self.task_list.append(self.current_experiment[i]["task_name"])
        if len(self.task_list) == 0:
            self.task_list_box.Set(['None'])
        else:
            self.task_list_box.Set(self.task_list)
            self.task_list_box.SetSelection(self.highlit_task_num)
        event.Skip()

    def Move_Down(self, event):  # wxGlade: MyFrame.<event_handler>
        if (self.highlit_task_num < len(self.task_list) - 1):
            self.current_experiment[self.highlit_task_num], self.current_experiment[self.highlit_task_num + 1] = self.current_experiment[self.highlit_task_num + 1], self.current_experiment[self.highlit_task_num]
            self.highlit_task_num = self.highlit_task_num + 1
        with open(self.experiment_folder+self.current_experiment_name+".pickle", "wb") as f:
            pickle.dump(self.current_experiment, f)
            f.close()
        # refresh task list
        del self.task_list[:]
        for i in range (0, len(self.current_experiment)):
            self.task_list.append(self.current_experiment[i]["task_name"])
        if len(self.task_list) == 0:
            self.task_list_box.Set(['None'])
        else:
            self.task_list_box.Set(self.task_list)
            self.task_list_box.SetSelection(self.highlit_task_num)
        event.Skip()

    def num_target_choose(self, event):  # wxGlade: MyFrame.<event_handler>       
        self.num_target_chosen = int(event.GetString())
        
        self.current_experiment[self.highlit_task_num]['num_targets'] = self.num_target_chosen
        ## Set num trial default
        if self.num_target_chosen > 2:
            self.num_trial_CB.SetValue(self.num_target_chosen)
            self.num_trial_mult = self.num_target_chosen
        elif self.num_target_chosen == 1:
            self.num_trial_CB.SetValue(3)
            self.num_trial_mult = 3
        elif self.num_target_chosen == 2:
            self.num_trial_CB.SetValue(4)
            self.num_trial_mult = 4
        self.current_experiment[self.highlit_task_num]['num_trials'] = self.num_trial_CB.GetValue()
        self.valid_trial_num = self.num_trial_CB.GetValue()
        ## SAVE
        with open(self.experiment_folder+self.current_experiment_name+".pickle", "wb") as f:
            pickle.dump(self.current_experiment, f)
            f.close()        
        event.Skip()
        

    def num_trial_choose(self, event):  # wxGlade: MyFrame.<event_handler>
        if event.GetInt() > self.valid_trial_num and event.GetInt() < (self.valid_trial_num + self.num_trial_mult):
            self.num_trial_CB.SetValue(self.valid_trial_num + self.num_trial_mult)
            self.valid_trial_num = self.valid_trial_num + self.num_trial_mult
        elif event.GetInt() < self.valid_trial_num and event.GetInt() > (self.valid_trial_num - self.num_trial_mult) and (self.valid_trial_num - self.num_trial_mult) > 0:
            self.num_trial_CB.SetValue(self.valid_trial_num - self.num_trial_mult)
            self.valid_trial_num = self.valid_trial_num - self.num_trial_mult
        else:
            self.num_trial_CB.SetValue(exp.myRounder(event.GetInt(), self.num_trial_mult))
            self.valid_trial_num =exp.myRounder(event.GetInt(), self.num_trial_mult)
        self.num_trial_chosen = self.valid_trial_num
        self.current_experiment[self.highlit_task_num]['num_trials'] = self.num_trial_chosen
        ## SAVE        
        with open(self.experiment_folder+self.current_experiment_name+".pickle", "wb") as f:
            pickle.dump(self.current_experiment, f)
            f.close()
        event.Skip()

    def rot_angle_choose(self, event):  # wxGlade: MyFrame.<event_handler>
        self.rotation_angle_chosen = int(event.GetString())
        self.current_experiment[self.highlit_task_num]['rotation_angle'] = self.rotation_angle_chosen
        with open(self.experiment_folder+self.current_experiment_name+".pickle", "wb") as f:
            pickle.dump(self.current_experiment, f)
            f.close()
        event.Skip()

    def Rot_Change_Press(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler 'Rot_Change_Press' not implemented!"
        event.Skip()

    def Lag_Enter(self, event):  # wxGlade: MyFrame.<event_handler>
        lag_conversion_factor = 37.2495/1000
        curr_string = event.GetString()
        if all(x in '0123456789' for x in curr_string):
            self.valid_lag_text = curr_string
        else:
            self.lag_txt.SetValue(self.valid_lag_text)
        if (event.GetString() == ''):
            self.current_experiment[self.highlit_task_num]['lag'] = 0
        else:
            self.current_experiment[self.highlit_task_num]['lag'] = int(int(event.GetString())*lag_conversion_factor)
            self.current_experiment[self.highlit_task_num]['lag_value'] = int(event.GetString())
        with open(self.experiment_folder+self.current_experiment_name+".pickle", "wb") as f:
            pickle.dump(self.current_experiment, f)
            f.close()
            
        event.Skip()

    def Pause_Enter(self, event):  # wxGlade: MyFrame.<event_handler>
        curr_string = event.GetString()
        if all(x in '0123456789' for x in curr_string):
            self.valid_pause_text = curr_string
        else:
            self.pause_txt.SetValue(self.valid_pause_text)
        if (event.GetString() == ''):
            self.current_experiment[self.highlit_task_num]['pausetime'] = 0
        else:
            self.current_experiment[self.highlit_task_num]['pausetime'] = int(event.GetString())
        with open(self.experiment_folder+self.current_experiment_name+".pickle", "wb") as f:
            pickle.dump(self.current_experiment, f)
            f.close()        
        event.Skip()

    def pause_message_make(self, event):  # wxGlade: MyFrame.<event_handler>
        self.current_experiment[self.highlit_task_num]['pause_instruction'] = event.GetString()
        with open(self.experiment_folder+self.current_experiment_name+".pickle", "wb") as f:
            pickle.dump(self.current_experiment, f)
            f.close()   
        event.Skip()
    
    def pause_check_press(self, event):
        self.current_experiment[self.highlit_task_num]['pause_button_wait'] = event.IsChecked()
        print event.IsChecked()        
        event.Skip()
    
    def target_distance_choose(self, event):
        event.Skip()
        
############################### EXPERIMENT CODE ##############################


# end of class MyFrame
class MyApp(wx.App):
    def OnInit(self):
        Virtuomotor = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(Virtuomotor)
        Virtuomotor.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name
    
    app = MyApp(0)
    app.MainLoop()
