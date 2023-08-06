# rtgym interfaces for Trackmania

# standard library imports
import platform
import logging
import time
from collections import deque

# third-party imports
import cv2
import gym.spaces as spaces
import numpy as np


# third-party imports
from rtgym import RealTimeGymInterface

# local imports
import tmrl.config.config_constants as cfg
from tmrl.custom.utils.compute_reward import RewardFunction
from tmrl.custom.utils.control_gamepad import control_gamepad, gamepad_reset, gamepad_close_finish_pop_up_tm20
from tmrl.custom.utils.control_keyboard import apply_control, keyres
from tmrl.custom.utils.control_mouse import mouse_close_finish_pop_up_tm20, mouse_save_replay_tm20
from tmrl.custom.utils.window import WindowInterface
from tmrl.custom.utils.tools import Lidar, TM2020OpenPlanetClient, get_speed, load_digits

# Globals ==============================================================================================================

NB_OBS_FORWARD = 500  # this allows (and rewards) 50m cuts

# Interface for Trackmania 2020 ========================================================================================


class TM2020Interface(RealTimeGymInterface):
    """
    This is the API needed for the algorithm to control Trackmania2020
    """
    def __init__(self, img_hist_len: int = 4, gamepad: bool = False, min_nb_steps_before_early_done: int = int(3.5 * 20), save_replay: bool = False):
        """
        Args:
        """
        self.last_time = None
        self.digits = None
        self.img_hist_len = img_hist_len
        self.img_hist = None
        self.img = None
        self.reward_function = None
        self.client = None
        self.gamepad = gamepad
        self.j = None
        self.window_interface = None
        self.small_window = None
        self.min_nb_steps_before_early_done = min_nb_steps_before_early_done
        self.save_replay = save_replay

        self.initialized = False

    def initialize_common(self):
        if self.gamepad:
            assert platform.system() == "Windows", "Sorry, Only Windows is supported for gamepad control"
            import vgamepad as vg
            self.j = vg.VX360Gamepad()
            logging.debug(" virtual joystick in use")
        self.window_interface = WindowInterface("Trackmania")
        self.window_interface.move_and_resize()
        self.last_time = time.time()
        self.digits = load_digits()
        self.img_hist = deque(maxlen=self.img_hist_len)
        self.img = None
        self.reward_function = RewardFunction(reward_data_path=cfg.REWARD_PATH,
                                              nb_obs_forward=NB_OBS_FORWARD,
                                              nb_obs_backward=10,
                                              nb_zero_rew_before_early_done=10,
                                              min_nb_steps_before_early_done=self.min_nb_steps_before_early_done)
        self.client = TM2020OpenPlanetClient()

    def initialize(self):
        self.initialize_common()
        self.small_window = True
        self.initialized = True

    def send_control(self, control):
        """
        Non-blocking function
        Applies the action given by the RL policy
        If control is None, does nothing (e.g. to record)
        Args:
            control: np.array: [forward,backward,right,left]
        """
        if self.gamepad:
            if control is not None:
                control_gamepad(self.j, control)
        else:
            if control is not None:
                actions = []
                if control[0] > 0:
                    actions.append('f')
                if control[1] > 0:
                    actions.append('b')
                if control[2] > 0.5:
                    actions.append('r')
                elif control[2] < -0.5:
                    actions.append('l')
                apply_control(actions)

    def grab_data_and_img(self):
        img = self.window_interface.screenshot()[:, :, :3]
        img = img[:, :, ::-1]  # reversed view for numpy RGB convention
        data = self.client.retrieve_data()
        self.img = img  # for render()
        return data, img

    def reset_race(self):
        if self.gamepad:
            gamepad_reset(self.j)
        else:
            keyres()

    def reset_common(self):
        if not self.initialized:
            self.initialize()
        self.send_control(self.get_default_action())
        self.reset_race()
        time_sleep = max(0, cfg.SLEEP_TIME_AT_RESET - 0.1) if self.gamepad else cfg.SLEEP_TIME_AT_RESET
        time.sleep(time_sleep)  # must be long enough for image to be refreshed

    def reset(self):
        """
        obs must be a list of numpy arrays
        """
        self.reset_common()
        data, img = self.grab_data_and_img()
        speed = np.array([
            data[0],
        ], dtype='float32')
        gear = np.array([
            data[9],
        ], dtype='float32')
        rpm = np.array([
            data[10],
        ], dtype='float32')
        for _ in range(self.img_hist_len):
            self.img_hist.append(img)
        imgs = np.array(list(self.img_hist))
        obs = [speed, gear, rpm, imgs]
        self.reward_function.reset()
        return obs

    def close_finish_pop_up_tm20(self):
        if self.gamepad:
            gamepad_close_finish_pop_up_tm20(self.j)
        else:
            mouse_close_finish_pop_up_tm20(small_window=self.small_window)

    def wait(self):
        """
        Non-blocking function
        The agent stays 'paused', waiting in position
        """
        self.send_control(self.get_default_action())
        self.reset_race()
        time.sleep(0.5)
        self.close_finish_pop_up_tm20()

    def get_obs_rew_done_info(self):
        """
        returns the observation, the reward, and a done signal for end of episode
        obs must be a list of numpy arrays
        """
        data, img = self.grab_data_and_img()
        speed = np.array([
            data[0],
        ], dtype='float32')
        gear = np.array([
            data[9],
        ], dtype='float32')
        rpm = np.array([
            data[10],
        ], dtype='float32')
        rew, done = self.reward_function.compute_reward(pos=np.array([data[2], data[3], data[4]]))
        rew = np.float32(rew)
        self.img_hist.append(img)
        imgs = np.array(list(self.img_hist))
        obs = [speed, gear, rpm, imgs]
        end_of_track = bool(data[8])
        info = {}
        if end_of_track:
            done = True
            info["__no_done"] = True  # TODO: we may want to remove this if we set an end-of-track reward
            if self.save_replay:
                mouse_save_replay_tm20(True)
        return obs, rew, done, info

    def get_observation_space(self):
        """
        must be a Tuple
        """
        speed = spaces.Box(low=0.0, high=1000.0, shape=(1, ))
        gear = spaces.Box(low=0.0, high=6, shape=(1, ))
        rpm = spaces.Box(low=0.0, high=np.inf, shape=(1, ))
        img = spaces.Box(low=0.0, high=255.0, shape=(self.img_hist_len, cfg.WINDOW_HEIGHT, cfg.WINDOW_WIDTH, 3))
        return spaces.Tuple((speed, gear, rpm, img))

    def get_action_space(self):
        """
        must return a Box
        """
        return spaces.Box(low=-1.0, high=1.0, shape=(3, ))

    def get_default_action(self):
        """
        initial action at episode start
        """
        return np.array([0.0, 0.0, 0.0], dtype='float32')


class TM2020InterfaceLidar(TM2020Interface):
    def __init__(self, img_hist_len=1, gamepad=False, min_nb_steps_before_early_done=int(20 * 3.5), record=False, save_replay: bool = False):
        super().__init__(img_hist_len, gamepad, min_nb_steps_before_early_done, save_replay)
        self.record = record
        self.window_interface = None
        self.lidar = None

    def grab_lidar_speed_and_data(self):
        img = self.window_interface.screenshot()[:, :, :3]
        data = self.client.retrieve_data()
        speed = np.array([
            data[0],
        ], dtype='float32')
        lidar = self.lidar.lidar_20(img=img, show=False)
        return lidar, speed, data

    def initialize(self):
        super().initialize_common()
        self.small_window = False
        self.lidar = Lidar(self.window_interface.screenshot())
        self.initialized = True

    def reset(self):
        """
        obs must be a list of numpy arrays
        """
        self.reset_common()
        img, speed, data = self.grab_lidar_speed_and_data()
        for _ in range(self.img_hist_len):
            self.img_hist.append(img)
        imgs = np.array(list(self.img_hist), dtype='float32')
        obs = [speed, imgs]
        self.reward_function.reset()
        return obs  # if not self.record else data

    def get_obs_rew_done_info(self):
        """
        returns the observation, the reward, and a done signal for end of episode
        obs must be a list of numpy arrays
        """
        img, speed, data = self.grab_lidar_speed_and_data()
        rew, done = self.reward_function.compute_reward(pos=np.array([data[2], data[3], data[4]]))
        rew = np.float32(rew)
        self.img_hist.append(img)
        imgs = np.array(list(self.img_hist), dtype='float32')
        obs = [speed, imgs]
        end_of_track = bool(data[8])
        info = {}
        if end_of_track:
            rew += cfg.REWARD_END_OF_TRACK
            done = True
            info["__no_done"] = True
            if self.save_replay:
                mouse_save_replay_tm20()
        rew += cfg.CONSTANT_PENALTY
        return obs, rew, done, info

    def get_observation_space(self):
        """
        must be a Tuple
        """
        speed = spaces.Box(low=0.0, high=1000.0, shape=(1, ))
        imgs = spaces.Box(low=0.0, high=np.inf, shape=(
            self.img_hist_len,
            19,
        ))  # lidars
        return spaces.Tuple((speed, imgs))


class TM2020InterfaceLidarProgress(TM2020InterfaceLidar):

    def reset(self):
        """
        obs must be a list of numpy arrays
        """
        self.reset_common()
        img, speed, data = self.grab_lidar_speed_and_data()
        for _ in range(self.img_hist_len):
            self.img_hist.append(img)
        imgs = np.array(list(self.img_hist), dtype='float32')
        progress = np.array([0], dtype='float32')
        obs = [speed, progress, imgs]
        self.reward_function.reset()
        return obs  # if not self.record else data

    def get_obs_rew_done_info(self):
        """
        returns the observation, the reward, and a done signal for end of episode
        obs must be a list of numpy arrays
        """
        img, speed, data = self.grab_lidar_speed_and_data()
        rew, done = self.reward_function.compute_reward(pos=np.array([data[2], data[3], data[4]]))
        progress = np.array([self.reward_function.cur_idx / self.reward_function.datalen], dtype='float32')
        rew = np.float32(rew)
        self.img_hist.append(img)
        imgs = np.array(list(self.img_hist), dtype='float32')
        obs = [speed, progress, imgs]
        end_of_track = bool(data[8])
        info = {}
        if end_of_track:
            rew += cfg.REWARD_END_OF_TRACK
            done = True
            info["__no_done"] = True
            if self.save_replay:
                mouse_save_replay_tm20()
        rew += cfg.CONSTANT_PENALTY
        return obs, rew, done, info

    def get_observation_space(self):
        """
        must be a Tuple
        """
        speed = spaces.Box(low=0.0, high=1000.0, shape=(1, ))
        progress = spaces.Box(low=0.0, high=1.0, shape=(1,))
        imgs = spaces.Box(low=0.0, high=np.inf, shape=(
            self.img_hist_len,
            19,
        ))  # lidars
        return spaces.Tuple((speed, progress, imgs))


# Interface for Trackmania Nations Forever: ============================================================================


class TMInterface(RealTimeGymInterface):
    """
    This is the API needed for the algorithm to control Trackmania Nations Forever
    """
    def __init__(self, img_hist_len=4):
        """
        Args:
        """
        self.window_interface = WindowInterface("Trackmania")
        self.last_time = time.time()
        self.digits = load_digits()
        self.img_hist_len = img_hist_len
        self.img_hist = deque(maxlen=self.img_hist_len)

    def send_control(self, control):
        """
        Non-blocking function
        Applies the action given by the RL policy
        If control is None, does nothing
        Args:
            control: np.array: [forward,backward,right,left]
        """
        if control is not None:
            actions = []
            if control[0] > 0:
                actions.append('f')
            if control[1] > 0:
                actions.append('b')
            if control[2] > 0.5:
                actions.append('r')
            elif control[2] < -0.5:
                actions.append('l')
            apply_control(actions)

    def grab_img_and_speed(self):
        img = self.window_interface.screenshot()[:, :, :3]
        speed = np.array([
            get_speed(img, self.digits),
        ], dtype='float32')
        img = img[100:-150, :]
        img = cv2.resize(img, (190, 50))
        # img = np.moveaxis(img, -1, 0)
        return img, speed

    def reset(self):
        """
        obs must be a list of numpy arrays
        """
        self.send_control(self.get_default_action())
        keyres()
        # time.sleep(0.05)  # must be long enough for image to be refreshed
        img, speed = self.grab_img_and_speed()
        for _ in range(self.img_hist_len):
            self.img_hist.append(img)
        imgs = np.array(list(self.img_hist), dtype='float32')
        obs = [speed, imgs]
        return obs

    def wait(self):
        """
        Non-blocking function
        The agent stays 'paused', waiting in position
        """
        self.send_control(self.get_default_action())

    def get_obs_rew_done_info(self):
        """
        returns the observation, the reward, and a done signal for end of episode
        obs must be a list of numpy arrays
        """
        img, speed = self.grab_img_and_speed()
        rew = speed[0]
        self.img_hist.append(img)
        imgs = np.array(list(self.img_hist), dtype='float32')
        obs = [speed, imgs]
        done = False  # TODO: True if race complete
        # logging.debug(f" len(obs):{len(obs)}, obs[0]:{obs[0]}, obs[1].shape:{obs[1].shape}")
        return obs, rew, done, {}

    def get_observation_space(self):
        """
        must be a Tuple
        """
        speed = spaces.Box(low=0.0, high=1000.0, shape=(1, ))
        imgs = spaces.Box(low=0.0, high=255.0, shape=(self.img_hist_len, 50, 190, 3))
        return spaces.Tuple((speed, imgs))

    def get_action_space(self):
        """
        must be a Box
        """
        return spaces.Box(low=-1.0, high=1.0, shape=(3, ))  # 1=f; 1=b; -1=l,+1=r

    def get_default_action(self):
        """
        initial action at episode start
        """
        return np.array([0.0, 0.0, 0.0], dtype='float32')


class TMInterfaceLidar(TMInterface):
    def __init__(self, img_hist_len=4):
        super().__init__(img_hist_len)
        self.lidar = Lidar(self.window_interface.screenshot())

    def grab_lidar_and_speed(self):
        img = self.window_interface.screenshot()[:, :, :3]
        speed = np.array([
            get_speed(img, self.digits),
        ], dtype='float32')
        lidar = self.lidar.lidar_20(img=img, show=False)
        return lidar, speed

    def reset(self):
        """
        obs must be a list of numpy arrays
        """
        self.send_control(self.get_default_action())
        keyres()
        # time.sleep(0.05)  # must be long enough for image to be refreshed
        img, speed = self.grab_lidar_and_speed()
        for _ in range(self.img_hist_len):
            self.img_hist.append(img)
        imgs = np.array(list(self.img_hist), dtype='float32')
        obs = [speed, imgs]
        return obs

    def get_obs_rew_done_info(self):
        """
        returns the observation, the reward, and a done signal for end of episode
        obs must be a list of numpy arrays
        """
        img, speed = self.grab_lidar_and_speed()
        rew = speed[0]
        self.img_hist.append(img)
        imgs = np.array(list(self.img_hist), dtype='float32')
        obs = [speed, imgs]
        done = False  # TODO: True if race complete
        # logging.debug(f" len(obs):{len(obs)}, obs[0]:{obs[0]}, obs[1].shape:{obs[1].shape}")
        return obs, rew, done, {}

    def get_observation_space(self):
        """
        must be a Tuple
        """
        speed = spaces.Box(low=0.0, high=1000.0, shape=(1, ))
        imgs = spaces.Box(low=0.0, high=np.inf, shape=(
            self.img_hist_len,
            19,
        ))  # lidars
        return spaces.Tuple((speed, imgs))


if __name__ == "__main__":
    pass
