#!/usr/bin/env python
"""
Created on 2017/3/3

@author: Yingjun Yang
"""
import time
from ctypes import c_uint8, c_uint16, c_uint32, c_uint64, pointer

from tool.device.library.load import Load
# from lib.utils.buf import Malloc
from utils.buf import Malloc

class Nexus(object):
    """
    IOCTL for nexus.ko
    """

    def __init__(self, dll, nexus_fd, nexus_dev):
        self.__dll = dll
        self.__nexus_fd = nexus_fd
        self.__nexus_dev = nexus_dev

    def read_ppalist_sync(self, addr, nlb, pdata, pmeta, plist, nsid=1, qid=1, dsmgmt=0, ctrl=0,
                          aeskey=0, aesenable=0, fmat=0):
        data = c_uint64(addr)
        return self.__dll.read_ppalist_sync(self.__nexus_fd, data, nlb, nsid, qid, dsmgmt, ctrl,
                                            pdata.buffer(), pmeta.buffer(), plist.buffer(),
                                            aeskey, aesenable, fmat)

    def read_ppalist_async(self, addr, nlb, plist, nsid=1, qid=1, dsmgmt=0, ctrl=0, aeskey=0,
                           aesenable=0, fmat=0):
        data = c_uint64(addr)
        return self.__dll.read_ppalist_async(self.__nexus_fd, data, nlb, nsid, qid, dsmgmt, ctrl,
                                             plist.buffer(), aeskey, aesenable, fmat)

    def write_ppalist_sync(self, addr, nlb, pdata, pmeta, plist, nsid=1, qid=1, dsmgmt=0, ctrl=0,
                           aeskey=0, aesenable=0, fmat=0, hint=0):
        data = c_uint64(addr)
        return self.__dll.write_ppalist_sync(self.__nexus_fd, data, nlb, nsid, qid, dsmgmt, ctrl,
                                             pdata.buffer(), pmeta.buffer(), plist.buffer(),
                                             aeskey, aesenable, fmat, hint)

    def write_ppalist_async(self, addr, nlb, plist, nsid=1, qid=1, dsmgmt=0, ctrl=0, aeskey=0,
                            aesenable=0, fmat=0, hint=0):
        data = c_uint64(addr)
        return self.__dll.write_ppalist_async(self.__nexus_fd, data, nlb, nsid, qid, dsmgmt, ctrl,
                                              plist.buffer(), aeskey, aesenable, fmat, hint)

    def read_pparawlist_sync(self, addr, nlb, pdata, pmeta, plist, nsid=1, qid=1, dsmgmt=0, ctrl=0,
                             aeskey=0, aesenable=0, fmat=0):
        data = c_uint64(addr)
        return self.__dll.read_pparawlist_sync(self.__nexus_fd, data, nlb, nsid, qid, dsmgmt, ctrl,
                                               pdata.buffer(), pmeta.buffer(), plist.buffer(),
                                               aeskey, aesenable, fmat)

    def write_pparawlist_sync(self, addr, nlb, pdata, pmeta, plist, nsid=1, qid=1, dsmgmt=0, ctrl=0,
                              aeskey=0, aesenable=0, fmat=0):
        data = c_uint64(addr)
        return self.__dll.write_pparawlist_sync(self.__nexus_fd, data, nlb, nsid, qid, dsmgmt, ctrl,
                                                pdata.buffer(), pmeta.buffer(), plist.buffer(),
                                                aeskey, aesenable, fmat)

    def erase_ppa_sync(self, addr, nlb, nsid=1, qid=1, ctrl=0):
        data = c_uint64(addr)
        return self.__dll.erase_ppa_sync(self.__nexus_fd, data, nlb, nsid, qid, ctrl)

    def read_register8(self, addr):
        data = c_uint32(0)
        if self.__dll.read_register8(self.__nexus_fd, addr, pointer(data)):
            raise RuntimeError("{}: read_register8 failed!".format(self.__nexus_dev))
        return data.value

    def write_register8(self, addr, value):
        return self.__dll.write_register8(self.__nexus_fd, addr, value)

    def read_register32(self, addr):
        data = c_uint32(0)
        if self.__dll.read_register32(self.__nexus_fd, addr, pointer(data)):
            raise RuntimeError("{}: read_register32 failed!".format(self.__nexus_dev))
        return data.value

    def write_register32(self, addr, value):
        return self.__dll.write_register32(self.__nexus_fd, addr, value)

    def read_register32bar4(self, addr):
        data = c_uint32(0)
        if self.__dll.read_register32bar4(self.__nexus_fd, addr, pointer(data)):
            raise RuntimeError("{}: read_register32bar4 failed!".format(self.__nexus_dev))
        else:
            return data.value

    def write_register32bar4(self, addr, value):
        return self.__dll.write_register32bar4(self.__nexus_fd, addr, value)

    def exp_rom_rw(self, addr, value, r_w):
        return self.__dll.exp_rom_rw(self.__nexus_fd, addr, value, r_w)

    def llrd_sync(self, addr, pdata, dirty=0, slot=0, retryhint=0, aeskey=0, aesenable=0,
                  dma_enable=1, mix=0):
        data = c_uint64(addr)
        return self.__dll.llrd_sync(self.__nexus_fd, data, dirty, slot, retryhint, aeskey,
                                    aesenable, dma_enable, mix, pdata.buffer())

    def starc_write(self, psrc, pdst, compare=0x1, aes_enable=0, aeskey=0, flags=0x0, nsid=1):
        return self.__dll.starc_write(self.__nexus_fd, nsid, aeskey, aes_enable,
                                      pdst.buffer(), psrc.buffer(), compare, flags)

    def starc_read(self, ndu, psrc, pdst, dcmp=0x1, aes_enable=0, aeskey=0, nsid=1):
        return self.__dll.starc_read(self.__nexus_fd, nsid, aeskey, aes_enable,
                                     pdst.buffer(), psrc.buffer(), ndu, dcmp)

    def tcg_download(self, ndw, offset, cdw15, pdata, cdw12=0x0F, cdw13=0x00, cdw14=0x00):
        return self.__dll.tcgDownload(self.__nexus_fd, ndw, offset, cdw15, cdw12, cdw13, cdw14,
                                      pdata.buffer())

    def llrs_info(self, slot):
        return self.__dll.llrs_info(self.__nexus_fd, slot)

    def write_spi(self, addr, pdata, nlb=1, nsid=1):
        data = c_uint64(addr)
        return self.__dll.write_spi(self.__nexus_fd, data, nlb, nsid, pdata.buffer())

    def read_spi(self, addr, pdata, nlb=1, nsid=1):
        data = c_uint64(addr)
        return self.__dll.read_spi(self.__nexus_fd, data, nlb, nsid, pdata.buffer())

    def get_cq(self, qid, pcq):
        status = self.__dll.get_cq(self.__nexus_fd, qid, pcq.buffer())
        if status:
            raise RuntimeError("{}: get_cq failed!".format(self.__nexus_dev))

    def get_sq(self, qid, psq):
        status = self.__dll.get_sq(self.__nexus_fd, qid, psq.buffer())
        if status:
            raise RuntimeError("{}: get_sq failed!".format(self.__nexus_dev))

    def write_register_space(self, addr, ndw, pdata, nsid=1, qid=1):
        data = c_uint64(addr)
        return self.__dll.writeRegSpace(self.__nexus_fd, data, ndw, nsid, qid, pdata.buffer())

    def read_register_space(self, addr, ndw, pdata, nsid=1, qid=1):
        data = c_uint64(addr)
        return self.__dll.readRegSpace(self.__nexus_fd, data, ndw, nsid, qid, pdata.buffer())

    def identify(self, cns, nsid=1, dword11=0, prpoff1=0, prpoff2=0):
        pdata = Malloc(length=4096, types=c_uint8)
        self.__dll.identify(self.__nexus_fd, cns, nsid, dword11, prpoff1, prpoff2, pdata.buffer())
        return pdata

    def format_nvm(self, nsid, cdw10):
        return self.__dll.format_nvm(self.__nexus_fd, nsid, cdw10)

    def create_sq(self, sqid, qsize=128, priority=1, contiguous=1, cqid=0):
        flag = contiguous + ((priority & 0x3) << 1)
        return self.__dll.create_sq(self.__nexus_fd, sqid, qsize, flag, cqid)

    def delete_sq(self, sqid):
        return self.__dll.delete_sq(self.__nexus_fd, sqid)

    def create_cq(self, cqid, irq_vector=0, irq_enable=1, qsize=128, rsvd1_0=0, rsvd1_1=0):
        return self.__dll.create_cq(
            self.__nexus_fd, cqid, irq_vector, irq_enable, qsize, rsvd1_0, rsvd1_1)

    def delete_cq(self, sqid):
        return self.__dll.delete_cq(self.__nexus_fd, sqid)

    def get_feature(self, nsid, fid, sel, pdata, dword11=0, prp1_off=0, prp2_off=0):
        return self.__dll.get_feature(self.__nexus_fd, nsid, fid, sel, dword11, prp1_off, prp2_off,
                                      pdata.buffer())

    def set_feature(self, nsid, fid, save, dword11, pdata, dword12=0, prp1_off=0, prp2_off=0):
        return self.__dll.set_feature(self.__nexus_fd, nsid, fid, save, dword11, dword12,
                                      prp1_off, prp2_off, pdata.buffer())

    def get_log_page(self, nsid, lid, ndw, prp1_off, prp2_off, pdata, lsi=0, lpo=0):
        return self.__dll.get_log_page(self.__nexus_fd, nsid, lid, ndw, lsi, prp1_off, prp2_off,
                                       pdata.buffer(), c_uint64(lpo))

    def directive_receive(self, nsid, ndw, doper, dtype, dspec, dword12, pdata, dword13=0,
                          prp_offset=0):
        return self.__dll.directive_receive(self.__nexus_fd, nsid, ndw, doper, dtype, dspec,
                                            dword12, dword13, prp_offset, pdata.buffer())

    def directive_send(self, nsid, ndw, doper, dtype, dspec, dword12, pdata, dword13=0,
                       prp_offset=0):
        return self.__dll.directive_send(self.__nexus_fd, nsid, ndw, doper, dtype, dspec,
                                         dword12, dword13, prp_offset, pdata.buffer())

    def abort(self, sqid, cid):
        return self.__dll.nvme_abort(self.__nexus_fd, sqid, cid)

    def self_test(self, stc, testaction=0):
        pass

    def get_event_request(self):
        return self.__dll.get_event_request(self.__nexus_fd)

    def namespace_create(self, nssize, nscap, flbas, setid=0, dps=0, nmic=0, agid=0):
        return self.__dll.namespace_create(self.__nexus_fd, nssize, nscap, flbas, setid,
                                           dps, nmic, agid)

    def namespace_delete(self, nsid):
        return self.__dll.namespace_delete(self.__nexus_fd, nsid)

    def namespace_attach(self, nsid, clist):
        num = len(clist)
        data = Malloc(2048, c_uint16)
        pdata = data.buffer()
        pdata[0] = num
        for i in range(0, num):
            pdata[i + 1] = clist[i]
        ret = self.__dll.namespace_attach(self.__nexus_fd, nsid, pdata)
        time.sleep(1)
        return ret

    def namespace_detach(self, nsid, clist):
        num = len(clist)
        data = Malloc(2048, c_uint16)
        pdata = data.buffer()
        pdata[0] = num
        for i in range(num):
            pdata[i + 1] = clist[i]
        return self.__dll.namespace_detach(self.__nexus_fd, nsid, pdata)

    def fw_download(self, ndw, offset, prp1_off, pdata):
        return self.__dll.fw_download(self.__nexus_fd, ndw, offset, prp1_off, pdata.buffer())

    def fw_active(self, slot, action, dw11):
        return self.__dll.fw_active(self.__nexus_fd, slot, action, dw11)

    def data_set(self, rangenum, pdata, attr, nsid=1, qid=1):
        return self.__dll.data_set(self.__nexus_fd, attr, rangenum, nsid, qid, pdata.buffer())

    def read_lba_sync(self, addr, nlb, pdata, pmeta, nsid=1, qid=1, ctrl=0, flags=0, reftag=0,
                      app_tag_and_mask=0):
        data = c_uint64(addr)
        return self.__dll.read_lba_sync(self.__nexus_fd, data, nlb, nsid, qid, ctrl, flags,
                                        reftag, app_tag_and_mask, pdata.buffer(), pmeta.buffer())

    def write_lba_sync(self, addr, nlb, pdata, pmeta, nsid=1, qid=1, ctrl=0, dir_spec=0,
                       flags=0, reftag=0, app_tag_and_mask=0, pi_bypass=0):
        data = c_uint64(addr)
        return self.__dll.write_lba_sync(self.__nexus_fd, data, nlb, nsid, qid, ctrl, dir_spec,
                                         flags, reftag, app_tag_and_mask, pi_bypass,
                                         pdata.buffer(), pmeta.buffer())

    def compare(self, addr, nlb, pdata, pmeta, nsid=1, qid=1, ctrl=0, flags=0, reftag=0,
                app_tag_and_mask=0):
        data = c_uint64(addr)
        return self.__dll.compare(self.__nexus_fd, data, nlb, nsid, qid, ctrl, flags, reftag,
                                  app_tag_and_mask, pdata.buffer(), pmeta.buffer())

    def verify(self, addr, nlb, nsid=1, qid=1, ctrl=0, flags=0, reftag=0, app_tag_and_mask=0):
        data = c_uint64(addr)
        return self.__dll.verify_sync(self.__nexus_fd, data, nlb, nsid, qid, ctrl, flags,
                                      reftag, app_tag_and_mask)

    def read_ppa_sgl_sync(self, addr, nlb, pdata, pmeta, psgldata, psglmeta, plist, d_desp_num,
                          m_desp_num, flags=0x80, nsid=1, qid=1, dsmgmt=0, ctrl=0, aeskey=0,
                          aesenable=0, fmt=0):
        data = c_uint64(addr)
        return self.__dll.read_ppa_sgl_sync(self.__nexus_fd, data, nlb, nsid, qid, dsmgmt, ctrl,
                                            pdata.buffer(), pmeta.buffer(), plist.buffer(),
                                            d_desp_num, m_desp_num, aeskey, aesenable, fmt, flags,
                                            psgldata.buffer(), psglmeta.buffer())

    def write_ppa_sgl_sync(self, addr, nlb, pdata, pmeta, psgldata, psglmeta, plist, d_desp_num,
                           m_desp_num, flags=0x80, nsid=1, qid=1, dsmgmt=0, ctrl=0, aeskey=0,
                           aesenable=0, fmt=0):
        data = c_uint64(addr)
        return self.__dll.write_ppa_sgl_sync(self.__nexus_fd, data, nlb, nsid, qid, dsmgmt, ctrl,
                                             pdata.buffer(), pmeta.buffer(), plist.buffer(),
                                             aeskey, aesenable, fmt, flags, psgldata.buffer(),
                                             psglmeta.buffer())

    def read_sgl_sync(self, addr, nlb, pdata, pmeta, psgldata, psglmeta, sgl_data_offset,
                      sgl_meta_offset, d_desp_num, m_desp_num, flags=0, reftag=0,
                      app_tag_and_mask=0, nsid=1, qid=1, dsmgmt=0, ctrl=0):
        data = c_uint64(addr)
        return self.__dll.read_sgl_sync(self.__nexus_fd, data, nlb, nsid, qid, dsmgmt, ctrl,
                                        flags, reftag, app_tag_and_mask, sgl_data_offset,
                                        sgl_meta_offset, d_desp_num, m_desp_num, pdata.buffer(),
                                        pmeta.buffer(), psgldata.buffer(), psglmeta.buffer())

    def write_sgl_sync(self, addr, nlb, pdata, pmeta, psgldata, psglmeta,
                       data_bucket_len, meta_bucket_len, sgl_data_offset,
                       sgl_meta_offset, d_desp_num, m_desp_num, flags=0,
                       reftag=0, app_tag_and_mask=0, nsid=1, qid=1, dsmgmt=0,
                       ctrl=0, dir_spec=0):
        """
        write LBA sync with SGL
        """
        data = c_uint64(addr)
        return self.__dll.write_sgl_sync(self.__nexus_fd, data, nlb, nsid, qid, dsmgmt,
                                         ctrl, dir_spec, flags, reftag, app_tag_and_mask,
                                         data_bucket_len, meta_bucket_len, sgl_data_offset,
                                         sgl_meta_offset, d_desp_num, m_desp_num, pdata.buffer(),
                                         pmeta.buffer(), psgldata.buffer(), psglmeta.buffer())

    def write_prp_sync(self, addr, nlb, pdata, prp_off, pmeta, nsid=1, qid=1, ctrl=0, dir_spec=0):
        data = c_uint64(addr)
        return self.__dll.write_prp_sync(self.__nexus_fd, data, nlb, nsid, qid, ctrl, dir_spec,
                                         pdata.buffer(), prp_off.buffer(), pmeta.buffer())

    def send_sqe(self, sqe_data, pdata, pmeta):
        return self.__dll.send_sqe(self.__nexus_fd, sqe_data.buffer(),
                                   pdata.buffer(), pmeta.buffer())

    def send_prp_sqe(self, sqe_data):
        return self.__dll.send_prp_sqe(self.__nexus_fd, sqe_data.buffer())

    def enable_db_switch(self):
        return self.__dll.enable_db_switch(self.__nexus_fd)

    def disable_db_switch(self):
        return self.__dll.disable_db_switch(self.__nexus_fd)

    def set_db_switch_rand(self):
        return self.__dll.set_db_switch_rand(self.__nexus_fd)

    def write_out_of_range_db_value(self):
        return self.__dll.write_out_of_range_db_value(self.__nexus_fd)

    def write_same_value_as_previous_db(self):
        return self.__dll.write_same_value_as_previous_db(self.__nexus_fd)

    def write_ppalist_async_latency(self, addr, nlb, pdata, pmeta, plist, ctrl,
                                    nsid=1, qid=1, dsmgmt=0, aeskey=0, aesenable=0, fmat=0):
        data = c_uint64(addr)
        return self.__dll.write_ppalist_async_latency(self.__nexus_fd, data, nlb,
                                                      nsid, qid, dsmgmt, ctrl,
                                                      pdata.buffer(), pmeta.buffer(),
                                                      plist.buffer(), aeskey, aesenable, fmat)

    def read_ppalist_sync_latency(self, addr, nlb, pdata, pmeta, plist, ctrl,
                                  nsid=1, qid=1, dsmgmt=0, aeskey=0, aesenable=0, fmat=0):
        data = c_uint64(addr)
        return self.__dll.read_ppalist_sync_latency(self.__nexus_fd, data, nlb,
                                                    nsid, qid, dsmgmt, ctrl,
                                                    pdata.buffer(), pmeta.buffer(),
                                                    plist.buffer(), aeskey, aesenable, fmat)

    def admin_passthru_sync(self, opcode, flags=0, nsid=1, cdw10=0, cdw11=0, cdw12=0,
                            cdw13=0, cdw14=0, cdw15=0):
        # cqe_dword0 = 0
        cqe_dword0 = c_uint32(0)
        # print("cqe_dword0 default value: 0x%x" % cqe_dword0)
        status = self.__dll.admin_pass_sync(self.__nexus_fd, opcode, flags, nsid, cdw10, cdw11,
                                            cdw12, cdw13, cdw14, cdw15, pointer(cqe_dword0))
        # print("cqe_dword0 update value: 0x%x; command status: 0x%x" % (cqe_dword0, status))
        return cqe_dword0.value, status

    def controller_reset(self, qid=0):
        return self.__dll.reset_with_level(self.__nexus_fd, 0x2, qid)

    def subsystem_reset(self, qid=0):
        return self.__dll.reset_with_level(self.__nexus_fd, 0x1, qid)

    def queue_level_reset(self, qid):
        return self.__dll.reset_with_level(self.__nexus_fd, 0x3, qid)


class Ktest(object):
    """
    IOCTL for ktest.ko
    """

    def __init__(self, dll, ktest_fd, ktest_dev):
        self.__dll = dll
        self.__ktest_fd = ktest_fd
        self.__ktest_dev = ktest_dev

    def get_async_cnt(self, pdata):
        return self.__dll.get_async_cnt(self.__ktest_fd, pdata.buffer())

    def clr_async_cnt(self):
        return self.__dll.clr_async_cnt(self.__ktest_fd)

    def get_async_err(self, pdata):
        return self.__dll.get_async_err_ppa(self.__ktest_fd, pdata.buffer())

    def clr_async_err(self):
        return self.__dll.clr_async_err_ppa(self.__ktest_fd)

    def read_ppa_list_async(self, addr, plist, nlb=1, nsid=1, qid=1,
                            dsmgmt=0, ctrl=0, index=0, addr_field=0):
        data = c_uint64(addr)
        return self.__dll.read_ppalist_async(self.__ktest_fd, data, nlb,
                                             nsid, qid, index, dsmgmt,
                                             ctrl, addr_field, plist.buffer())

    def write_ppa_list_async(self, addr, pdata, pmeta, plist, nlb=1, nsid=1,
                             qid=1, dsmgmt=0, ctrl=0, addr_field=0,
                             index=0, dat_flag=0, hint=0):
        data = c_uint64(addr)
        return self.__dll.write_ppalist_async(self.__ktest_fd, data, nlb, nsid,
                                              qid, index, dsmgmt, ctrl, addr_field,
                                              pdata.buffer(), pmeta.buffer(),
                                              plist.buffer(), dat_flag, hint)

    def read_ppa_async(self, addr, nlb=1, nsid=1, qid=1, dsmgmt=0, ctrl=0, index=0, addr_field=0):
        data = c_uint64(addr)
        return self.__dll.read_ppa_async(self.__ktest_fd, data, nlb, nsid, qid, index, dsmgmt, ctrl,
                                         addr_field)

    def write_ppa_async(self, addr, pdata, pmeta, nlb=1, nsid=1, qid=1, dsmgmt=0, ctrl=0,
                        addr_field=0, index=0, dat_flag=1):
        data = c_uint64(addr)
        return self.__dll.write_ppa_async(self.__ktest_fd, data, nlb, nsid, qid, index, dsmgmt,
                                          ctrl, addr_field, pdata.buffer(), pmeta.buffer(),
                                          dat_flag)

    def read_lba_async(self, addr, pdata, pmeta, nlb=1, nsid=1, qid=1, ctrl=0):
        data = c_uint64(addr)
        return self.__dll.read_lba_async(self.__ktest_fd, data, nlb, nsid, qid, ctrl,
                                         pdata.buffer(), pmeta.buffer())

    def write_lba_async(self, addr, pdata, pmeta, nlb=1, nsid=1, qid=1, ctrl=0):
        data = c_uint64(addr)
        return self.__dll.write_lba_async(self.__ktest_fd, data, nlb, nsid, qid, ctrl,
                                          pdata.buffer(), pmeta.buffer())

    def atomic_async_test(self, addr, nlb=1, nsid=1, qid=1, rd_flg=0, pat=0):
        """
        read LBA async compare test
        ctrl: 0, non-coherence mode
              1, coherence mode
        """
        data = c_uint64(addr)
        return self.__dll.qat_atomic(self.__ktest_fd, data, nlb, nsid, qid, rd_flg, pat)

    def read_async_test(self, addr, nlb=1, nsid=1, qid=1, ctrl=0):
        """
        read LBA async compare test
        ctrl: 0, non-coherence mode
              1, coherence mode
        """
        data = c_uint64(addr)
        return self.__dll.read_lba_async_test(self.__ktest_fd, data, nlb, nsid, qid, ctrl)

    def write_async_test(self, addr, nlb=1, nsid=1, qid=1, ctrl=0):
        """
        write LBA async compare test
        ctrl: 0, non-coherence mode
              1, coherence mode
        """
        data = c_uint64(addr)
        return self.__dll.write_lba_async_test(self.__ktest_fd, data, nlb, nsid, qid, ctrl)

    def write_xor_sync(self, addr, nsid=1, qid=1, index=0, dsmgmt=0, ctrl=0):
        data = c_uint64(addr)
        return self.__dll.write_xor_sync(self.__ktest_fd, data, nsid, qid, index, dsmgmt, ctrl)

    def read_xor_sync(self, addr, pdata, nsid=1, qid=1, index=0, dsmgmt=0, ctrl=0):
        data = c_uint64(addr)
        return self.__dll.read_xor_sync(self.__ktest_fd, data, nsid, qid, index, dsmgmt,
                                        ctrl, pdata.buffer())

    def load_xor_sync(self, addr, nsid=1, qid=1, index=0, dsmgmt=0, ctrl=0):
        data = c_uint64(addr)
        return self.__dll.load_xor_sync(self.__ktest_fd, data, nsid, qid, index, dsmgmt, ctrl)

    def write_xor_async(self, addr, nsid=1, qid=1, index=0, dsmgmt=0, ctrl=0):
        data = c_uint64(addr)
        return self.__dll.write_xor_async(self.__ktest_fd, data, nsid, qid, index, dsmgmt, ctrl)

    def read_xor_async(self, addr, pdata, nsid=1, qid=1, index=0, dsmgmt=0, ctrl=0):
        data = c_uint64(addr)
        return self.__dll.read_xor_async(self.__ktest_fd, data, nsid, qid, index, dsmgmt,
                                         ctrl, pdata.buffer())

    def load_xor_async(self, addr, nsid=1, qid=1, index=0, dsmgmt=0, ctrl=0):
        data = c_uint64(addr)
        return self.__dll.load_xor_async(self.__ktest_fd, data, nsid, qid, index, dsmgmt, ctrl)

    @staticmethod
    def flush(nsid=1, qid=1):
        raise RuntimeError("ioctl flush is not implemented")
        # return self.__dll.flush(nsid, qid)

    def write_zeroes(self, addr, nlb, pdata, pmeta, nsid=1, qid=1, ctrl=0, reftag=0,
                     app_tag_and_mask=0):
        # data = c_uint64(addr)
        return self.__dll.write_zeroes(self.__ktest_fd, addr, nlb, nsid, qid, ctrl,
                                       reftag, app_tag_and_mask, pdata.buffer(), pmeta.buffer())

    def write_unco(self, addr, nlb, nsid=1, qid=1):
        data = c_uint64(addr)
        return self.__dll.write_uncorrectable(self.__ktest_fd, data, nlb, nsid, qid)

    def read_ppalist_mapping(self, addr, nlb, opcode, pdata, pmeta, plist, nsid=1, qid=1,
                             dsmgmt=0, ctrl=0, aeskey=0, aesenable=0, fmat=0):
        data = c_uint64(addr)
        return self.__dll.read_ppalist_sync_mapping_opcode(
            self.__ktest_fd, data, nlb, nsid, qid, dsmgmt, ctrl, opcode, pdata.buffer(),
            pmeta.buffer(), plist.buffer(), aeskey, aesenable, fmat)


class Ioctl(Nexus, Ktest):
    """
    IOCTL for CNEX driver, include nexus.ko and ktest.ko
    """

    def __init__(self, nexus="/dev/nexus0", ktest="/dev/ktest0"):
        load = Load()
        self.__nexus_dev = None
        self.__ktest_dev = None
        self.__dll = load.cdll_dev()

        # load nexus driver
        self.__nexus_fd = self.__dll.openDev(nexus.encode(encoding="utf-8"))
        if self.__nexus_fd == -1:
            raise RuntimeError("open device({}, {}) failed!".format(nexus, self.__nexus_fd))
        self.__nexus_dev = nexus
        Nexus.__init__(self, self.__dll, self.__nexus_fd, self.__nexus_dev)

        # load ktest
        if ktest:
            self.__ktest_fd = self.__dll.openDev(ktest.encode(encoding="utf-8"))
            if self.__ktest_fd == -1:
                raise RuntimeError("open device({}, {}) failed!".format(ktest, self.__ktest_fd))
            self.__ktest_dev = ktest
            Ktest.__init__(self, self.__dll, self.__ktest_fd, self.__ktest_dev)

    def __del__(self):
        # close nexus
        if self.__nexus_dev:
            if self.__dll.close_dev(self.__nexus_fd):
                raise RuntimeError("close device({}) failed!".format(self.__nexus_dev))
            del self.__nexus_fd
            self.__nexus_dev = None

        # close ktest
        if self.__ktest_dev:
            if self.__dll.close_dev(self.__ktest_fd):
                raise RuntimeError("close device({}) failed!".format(self.__ktest_dev))
            del self.__ktest_fd
            self.__ktest_dev = None

    def close_dev(self):
        self.__del__()
