/* This file was generated from the templator_front.org org-mode file.
   To generate it, open templator_front.org in Emacs and execute
   M-x org-babel-tangle
*/

#ifndef TREXIO_H
#define TREXIO_H

#include <stdbool.h>
#include <stdint.h>
  #define HAVE_HDF5 1

typedef int32_t trexio_exit_code;

#define TREXIO_FAILURE                 ((trexio_exit_code) -1)
#define TREXIO_SUCCESS                 ((trexio_exit_code) 0)
#define TREXIO_INVALID_ARG_1           ((trexio_exit_code) 1)
#define TREXIO_INVALID_ARG_2           ((trexio_exit_code) 2)
#define TREXIO_INVALID_ARG_3           ((trexio_exit_code) 3)
#define TREXIO_INVALID_ARG_4           ((trexio_exit_code) 4)
#define TREXIO_INVALID_ARG_5           ((trexio_exit_code) 5)
#define TREXIO_END                     ((trexio_exit_code) 6)
#define TREXIO_READONLY                ((trexio_exit_code) 7)
#define TREXIO_ERRNO                   ((trexio_exit_code) 8)
#define TREXIO_INVALID_ID              ((trexio_exit_code) 9)
#define TREXIO_ALLOCATION_FAILED       ((trexio_exit_code) 10)
#define TREXIO_HAS_NOT                 ((trexio_exit_code) 11)
#define TREXIO_INVALID_NUM             ((trexio_exit_code) 12)
#define TREXIO_ATTR_ALREADY_EXISTS     ((trexio_exit_code) 13)
#define TREXIO_DSET_ALREADY_EXISTS     ((trexio_exit_code) 14)
#define TREXIO_OPEN_ERROR              ((trexio_exit_code) 15)
#define TREXIO_LOCK_ERROR              ((trexio_exit_code) 16)
#define TREXIO_UNLOCK_ERROR            ((trexio_exit_code) 17)
#define TREXIO_FILE_ERROR              ((trexio_exit_code) 18)
#define TREXIO_GROUP_READ_ERROR        ((trexio_exit_code) 19)
#define TREXIO_GROUP_WRITE_ERROR       ((trexio_exit_code) 20)
#define TREXIO_ELEM_READ_ERROR         ((trexio_exit_code) 21)
#define TREXIO_ELEM_WRITE_ERROR        ((trexio_exit_code) 22)
#define TREXIO_UNSAFE_ARRAY_DIM        ((trexio_exit_code) 23)
#define TREXIO_ATTR_MISSING            ((trexio_exit_code) 24)
#define TREXIO_DSET_MISSING            ((trexio_exit_code) 25)
#define TREXIO_BACK_END_MISSING        ((trexio_exit_code) 26)
#define TREXIO_INVALID_ARG_6           ((trexio_exit_code) 27)
#define TREXIO_INVALID_ARG_7           ((trexio_exit_code) 28)
#define TREXIO_INVALID_ARG_8           ((trexio_exit_code) 29)
#define TREXIO_INVALID_STR_LEN         ((trexio_exit_code) 30)
#define TREXIO_INT_SIZE_OVERFLOW       ((trexio_exit_code) 31)
#define TREXIO_SAFE_MODE               ((trexio_exit_code) 32)
#define TREXIO_INVALID_ELECTRON_NUM    ((trexio_exit_code) 33)
#define TREXIO_INVALID_DETERMINANT_NUM ((trexio_exit_code) 34)
#define TREXIO_INVALID_STATE           ((trexio_exit_code) 35)
#define TREXIO_VERSION_PARSING_ISSUE   ((trexio_exit_code) 36)

const char* trexio_string_of_error(const trexio_exit_code error);
void trexio_string_of_error_f(const trexio_exit_code error, char result[128]);

typedef int32_t back_end_t;

#define TREXIO_HDF5             ( (back_end_t) 0 )
#define TREXIO_TEXT             ( (back_end_t) 1 )
#define TREXIO_INVALID_BACK_END ( (back_end_t) 2 )
#define TREXIO_AUTO             TREXIO_INVALID_BACK_END
/*#define TREXIO_JSON             ( (back_end_t) 2 )*/

#define TREXIO_DELIM            "\n"

bool trexio_has_backend(back_end_t back_end);
bool trexio_has_back_end(back_end_t back_end);

typedef struct trexio_s trexio_t;

trexio_t* trexio_open(const char* file_name, const char mode,
                      const back_end_t back_end, trexio_exit_code* const rc_open);

trexio_exit_code trexio_set_one_based(trexio_t* file);

trexio_exit_code trexio_close(trexio_t* file);

trexio_exit_code trexio_inquire(const char* file_name);

trexio_exit_code trexio_set_state(trexio_t* file, const int32_t num);
trexio_exit_code trexio_get_state(trexio_t* file, int32_t* const num);

trexio_exit_code trexio_info(void);
trexio_exit_code trexio_mark_safety(trexio_t* const file, const int32_t safety_flag);

typedef int64_t  bitfield_t;

#define TREXIO_ORBITAL_SHIFT  1
#define TREXIO_INT_SIZE       64
#define TREXIO_NORB_PER_INT   ( 8*sizeof(bitfield_t) )
#
trexio_exit_code trexio_to_orbital_list (const int32_t N_int, const bitfield_t* d1, int32_t* const list, int32_t* const occupied_num);
trexio_exit_code trexio_to_orbital_list_up_dn (const int32_t N_int, const bitfield_t* d1, int32_t* const list_up, int32_t* const list_dn, int32_t* const occ_num_up, int32_t* const occ_num_dn);
trexio_exit_code trexio_safe_to_orbital_list (const int32_t N_int, const bitfield_t* dset_in, const int64_t dim_in, int32_t* const dset_out, const int64_t dim_out, int32_t* const num);
trexio_exit_code trexio_safe_to_orbital_list_up_dn (const int32_t N_int, const bitfield_t* dset_in, const int64_t dim_in, int32_t* const dset_up_out, const int64_t dim_up_out, int32_t* const dset_dn_out, const int64_t dim_dn_out, int32_t* const num_up, int32_t* const num_dn);

#define TREXIO_PACKAGE_VERSION "2.2.0"
#define TREXIO_VERSION_MAJOR 2
#define TREXIO_VERSION_MINOR 2
#define TREXIO_VERSION_PATCH 0
#define TREXIO_GIT_HASH "4f07eb095355969712cd64c1ada447df9ef48ff8"

trexio_exit_code trexio_delete_metadata(trexio_t* const file);

trexio_exit_code trexio_delete_electron(trexio_t* const file);

trexio_exit_code trexio_delete_nucleus(trexio_t* const file);

trexio_exit_code trexio_delete_ecp(trexio_t* const file);

trexio_exit_code trexio_delete_basis(trexio_t* const file);

trexio_exit_code trexio_delete_ao(trexio_t* const file);

trexio_exit_code trexio_delete_ao_1e_int(trexio_t* const file);

trexio_exit_code trexio_delete_ao_2e_int(trexio_t* const file);

trexio_exit_code trexio_delete_mo(trexio_t* const file);

trexio_exit_code trexio_delete_mo_1e_int(trexio_t* const file);

trexio_exit_code trexio_delete_mo_2e_int(trexio_t* const file);

trexio_exit_code trexio_delete_determinant(trexio_t* const file);

trexio_exit_code trexio_delete_state(trexio_t* const file);

trexio_exit_code trexio_delete_rdm(trexio_t* const file);

trexio_exit_code trexio_delete_cell(trexio_t* const file);

trexio_exit_code trexio_delete_pbc(trexio_t* const file);

trexio_exit_code trexio_delete_qmc(trexio_t* const file);

trexio_exit_code trexio_has_metadata_code_num(trexio_t* const file);
trexio_exit_code trexio_read_metadata_code_num(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_metadata_code_num(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_metadata_code_num_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_metadata_code_num_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_metadata_code_num_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_metadata_code_num_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_metadata_author_num(trexio_t* const file);
trexio_exit_code trexio_read_metadata_author_num(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_metadata_author_num(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_metadata_author_num_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_metadata_author_num_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_metadata_author_num_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_metadata_author_num_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_metadata_unsafe(trexio_t* const file);
trexio_exit_code trexio_read_metadata_unsafe(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_metadata_unsafe(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_metadata_unsafe_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_metadata_unsafe_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_metadata_unsafe_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_metadata_unsafe_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_electron_num(trexio_t* const file);
trexio_exit_code trexio_read_electron_num(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_electron_num(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_electron_num_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_electron_num_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_electron_num_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_electron_num_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_electron_up_num(trexio_t* const file);
trexio_exit_code trexio_read_electron_up_num(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_electron_up_num(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_electron_up_num_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_electron_up_num_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_electron_up_num_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_electron_up_num_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_electron_dn_num(trexio_t* const file);
trexio_exit_code trexio_read_electron_dn_num(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_electron_dn_num(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_electron_dn_num_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_electron_dn_num_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_electron_dn_num_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_electron_dn_num_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_nucleus_num(trexio_t* const file);
trexio_exit_code trexio_read_nucleus_num(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_nucleus_num(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_nucleus_num_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_nucleus_num_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_nucleus_num_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_nucleus_num_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_nucleus_repulsion(trexio_t* const file);
trexio_exit_code trexio_read_nucleus_repulsion(trexio_t* const file, double* const num);
trexio_exit_code trexio_write_nucleus_repulsion(trexio_t* const file, const double num);
trexio_exit_code trexio_read_nucleus_repulsion_32(trexio_t* const file, float* const num);
trexio_exit_code trexio_write_nucleus_repulsion_32(trexio_t* const file, const float num);
trexio_exit_code trexio_read_nucleus_repulsion_64(trexio_t* const file, double* const num);
trexio_exit_code trexio_write_nucleus_repulsion_64(trexio_t* const file, const double num);

trexio_exit_code trexio_has_ecp_num(trexio_t* const file);
trexio_exit_code trexio_read_ecp_num(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_ecp_num(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_ecp_num_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_ecp_num_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_ecp_num_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_ecp_num_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_basis_prim_num(trexio_t* const file);
trexio_exit_code trexio_read_basis_prim_num(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_basis_prim_num(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_basis_prim_num_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_basis_prim_num_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_basis_prim_num_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_basis_prim_num_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_basis_shell_num(trexio_t* const file);
trexio_exit_code trexio_read_basis_shell_num(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_basis_shell_num(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_basis_shell_num_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_basis_shell_num_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_basis_shell_num_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_basis_shell_num_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_ao_cartesian(trexio_t* const file);
trexio_exit_code trexio_read_ao_cartesian(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_ao_cartesian(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_ao_cartesian_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_ao_cartesian_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_ao_cartesian_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_ao_cartesian_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_ao_num(trexio_t* const file);
trexio_exit_code trexio_read_ao_num(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_ao_num(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_ao_num_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_ao_num_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_ao_num_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_ao_num_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_mo_num(trexio_t* const file);
trexio_exit_code trexio_read_mo_num(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_mo_num(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_mo_num_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_mo_num_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_mo_num_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_mo_num_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_determinant_num(trexio_t* const file);
trexio_exit_code trexio_read_determinant_num(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_read_determinant_num_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_read_determinant_num_64(trexio_t* const file, int64_t* const num);

trexio_exit_code trexio_has_state_num(trexio_t* const file);
trexio_exit_code trexio_read_state_num(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_state_num(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_state_num_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_state_num_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_state_num_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_state_num_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_pbc_periodic(trexio_t* const file);
trexio_exit_code trexio_read_pbc_periodic(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_pbc_periodic(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_pbc_periodic_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_pbc_periodic_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_pbc_periodic_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_pbc_periodic_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_qmc_num(trexio_t* const file);
trexio_exit_code trexio_read_qmc_num(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_qmc_num(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_qmc_num_32(trexio_t* const file, int32_t* const num);
trexio_exit_code trexio_write_qmc_num_32(trexio_t* const file, const int32_t num);
trexio_exit_code trexio_read_qmc_num_64(trexio_t* const file, int64_t* const num);
trexio_exit_code trexio_write_qmc_num_64(trexio_t* const file, const int64_t num);

trexio_exit_code trexio_has_metadata_package_version(trexio_t* const file);
trexio_exit_code trexio_read_metadata_package_version(trexio_t* const file, char* const str_out, const int32_t max_str_len);
trexio_exit_code trexio_write_metadata_package_version(trexio_t* const file, const char* str, const int32_t max_str_len);

trexio_exit_code trexio_has_metadata_description(trexio_t* const file);
trexio_exit_code trexio_read_metadata_description(trexio_t* const file, char* const str_out, const int32_t max_str_len);
trexio_exit_code trexio_write_metadata_description(trexio_t* const file, const char* str, const int32_t max_str_len);

trexio_exit_code trexio_has_nucleus_point_group(trexio_t* const file);
trexio_exit_code trexio_read_nucleus_point_group(trexio_t* const file, char* const str_out, const int32_t max_str_len);
trexio_exit_code trexio_write_nucleus_point_group(trexio_t* const file, const char* str, const int32_t max_str_len);

trexio_exit_code trexio_has_basis_type(trexio_t* const file);
trexio_exit_code trexio_read_basis_type(trexio_t* const file, char* const str_out, const int32_t max_str_len);
trexio_exit_code trexio_write_basis_type(trexio_t* const file, const char* str, const int32_t max_str_len);

trexio_exit_code trexio_has_mo_type(trexio_t* const file);
trexio_exit_code trexio_read_mo_type(trexio_t* const file, char* const str_out, const int32_t max_str_len);
trexio_exit_code trexio_write_mo_type(trexio_t* const file, const char* str, const int32_t max_str_len);

trexio_exit_code trexio_has_nucleus_charge(trexio_t* const file);
trexio_exit_code trexio_read_nucleus_charge(trexio_t* const file, double* const nucleus_charge);
trexio_exit_code trexio_write_nucleus_charge(trexio_t* const file, const double* nucleus_charge);
trexio_exit_code trexio_read_nucleus_charge_32(trexio_t* const file, float* const nucleus_charge);
trexio_exit_code trexio_write_nucleus_charge_32(trexio_t* const file, const float* nucleus_charge);
trexio_exit_code trexio_read_nucleus_charge_64(trexio_t* const file, double* const nucleus_charge);
trexio_exit_code trexio_write_nucleus_charge_64(trexio_t* const file, const double* nucleus_charge);
trexio_exit_code trexio_read_safe_nucleus_charge(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_nucleus_charge(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_nucleus_charge_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_nucleus_charge_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_nucleus_charge_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_nucleus_charge_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_nucleus_coord(trexio_t* const file);
trexio_exit_code trexio_read_nucleus_coord(trexio_t* const file, double* const nucleus_coord);
trexio_exit_code trexio_write_nucleus_coord(trexio_t* const file, const double* nucleus_coord);
trexio_exit_code trexio_read_nucleus_coord_32(trexio_t* const file, float* const nucleus_coord);
trexio_exit_code trexio_write_nucleus_coord_32(trexio_t* const file, const float* nucleus_coord);
trexio_exit_code trexio_read_nucleus_coord_64(trexio_t* const file, double* const nucleus_coord);
trexio_exit_code trexio_write_nucleus_coord_64(trexio_t* const file, const double* nucleus_coord);
trexio_exit_code trexio_read_safe_nucleus_coord(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_nucleus_coord(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_nucleus_coord_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_nucleus_coord_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_nucleus_coord_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_nucleus_coord_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ecp_max_ang_mom_plus_1(trexio_t* const file);
trexio_exit_code trexio_read_ecp_max_ang_mom_plus_1(trexio_t* const file, int32_t* const ecp_max_ang_mom_plus_1);
trexio_exit_code trexio_write_ecp_max_ang_mom_plus_1(trexio_t* const file, const int32_t* ecp_max_ang_mom_plus_1);
trexio_exit_code trexio_read_ecp_max_ang_mom_plus_1_32(trexio_t* const file, int32_t* const ecp_max_ang_mom_plus_1);
trexio_exit_code trexio_write_ecp_max_ang_mom_plus_1_32(trexio_t* const file, const int32_t* ecp_max_ang_mom_plus_1);
trexio_exit_code trexio_read_ecp_max_ang_mom_plus_1_64(trexio_t* const file, int64_t* const ecp_max_ang_mom_plus_1);
trexio_exit_code trexio_write_ecp_max_ang_mom_plus_1_64(trexio_t* const file, const int64_t* ecp_max_ang_mom_plus_1);
trexio_exit_code trexio_read_safe_ecp_max_ang_mom_plus_1(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_max_ang_mom_plus_1(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ecp_max_ang_mom_plus_1_32(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_max_ang_mom_plus_1_32(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ecp_max_ang_mom_plus_1_64(trexio_t* const file, int64_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_max_ang_mom_plus_1_64(trexio_t* const file, const int64_t* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ecp_z_core(trexio_t* const file);
trexio_exit_code trexio_read_ecp_z_core(trexio_t* const file, int32_t* const ecp_z_core);
trexio_exit_code trexio_write_ecp_z_core(trexio_t* const file, const int32_t* ecp_z_core);
trexio_exit_code trexio_read_ecp_z_core_32(trexio_t* const file, int32_t* const ecp_z_core);
trexio_exit_code trexio_write_ecp_z_core_32(trexio_t* const file, const int32_t* ecp_z_core);
trexio_exit_code trexio_read_ecp_z_core_64(trexio_t* const file, int64_t* const ecp_z_core);
trexio_exit_code trexio_write_ecp_z_core_64(trexio_t* const file, const int64_t* ecp_z_core);
trexio_exit_code trexio_read_safe_ecp_z_core(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_z_core(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ecp_z_core_32(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_z_core_32(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ecp_z_core_64(trexio_t* const file, int64_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_z_core_64(trexio_t* const file, const int64_t* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ecp_ang_mom(trexio_t* const file);
trexio_exit_code trexio_read_ecp_ang_mom(trexio_t* const file, int32_t* const ecp_ang_mom);
trexio_exit_code trexio_write_ecp_ang_mom(trexio_t* const file, const int32_t* ecp_ang_mom);
trexio_exit_code trexio_read_ecp_ang_mom_32(trexio_t* const file, int32_t* const ecp_ang_mom);
trexio_exit_code trexio_write_ecp_ang_mom_32(trexio_t* const file, const int32_t* ecp_ang_mom);
trexio_exit_code trexio_read_ecp_ang_mom_64(trexio_t* const file, int64_t* const ecp_ang_mom);
trexio_exit_code trexio_write_ecp_ang_mom_64(trexio_t* const file, const int64_t* ecp_ang_mom);
trexio_exit_code trexio_read_safe_ecp_ang_mom(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_ang_mom(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ecp_ang_mom_32(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_ang_mom_32(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ecp_ang_mom_64(trexio_t* const file, int64_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_ang_mom_64(trexio_t* const file, const int64_t* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ecp_nucleus_index(trexio_t* const file);
trexio_exit_code trexio_read_ecp_nucleus_index(trexio_t* const file, int32_t* const ecp_nucleus_index);
trexio_exit_code trexio_write_ecp_nucleus_index(trexio_t* const file, const int32_t* ecp_nucleus_index);
trexio_exit_code trexio_read_ecp_nucleus_index_32(trexio_t* const file, int32_t* const ecp_nucleus_index);
trexio_exit_code trexio_write_ecp_nucleus_index_32(trexio_t* const file, const int32_t* ecp_nucleus_index);
trexio_exit_code trexio_read_ecp_nucleus_index_64(trexio_t* const file, int64_t* const ecp_nucleus_index);
trexio_exit_code trexio_write_ecp_nucleus_index_64(trexio_t* const file, const int64_t* ecp_nucleus_index);
trexio_exit_code trexio_read_safe_ecp_nucleus_index(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_nucleus_index(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ecp_nucleus_index_32(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_nucleus_index_32(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ecp_nucleus_index_64(trexio_t* const file, int64_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_nucleus_index_64(trexio_t* const file, const int64_t* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ecp_exponent(trexio_t* const file);
trexio_exit_code trexio_read_ecp_exponent(trexio_t* const file, double* const ecp_exponent);
trexio_exit_code trexio_write_ecp_exponent(trexio_t* const file, const double* ecp_exponent);
trexio_exit_code trexio_read_ecp_exponent_32(trexio_t* const file, float* const ecp_exponent);
trexio_exit_code trexio_write_ecp_exponent_32(trexio_t* const file, const float* ecp_exponent);
trexio_exit_code trexio_read_ecp_exponent_64(trexio_t* const file, double* const ecp_exponent);
trexio_exit_code trexio_write_ecp_exponent_64(trexio_t* const file, const double* ecp_exponent);
trexio_exit_code trexio_read_safe_ecp_exponent(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_exponent(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ecp_exponent_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_exponent_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ecp_exponent_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_exponent_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ecp_coefficient(trexio_t* const file);
trexio_exit_code trexio_read_ecp_coefficient(trexio_t* const file, double* const ecp_coefficient);
trexio_exit_code trexio_write_ecp_coefficient(trexio_t* const file, const double* ecp_coefficient);
trexio_exit_code trexio_read_ecp_coefficient_32(trexio_t* const file, float* const ecp_coefficient);
trexio_exit_code trexio_write_ecp_coefficient_32(trexio_t* const file, const float* ecp_coefficient);
trexio_exit_code trexio_read_ecp_coefficient_64(trexio_t* const file, double* const ecp_coefficient);
trexio_exit_code trexio_write_ecp_coefficient_64(trexio_t* const file, const double* ecp_coefficient);
trexio_exit_code trexio_read_safe_ecp_coefficient(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_coefficient(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ecp_coefficient_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_coefficient_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ecp_coefficient_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_coefficient_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ecp_power(trexio_t* const file);
trexio_exit_code trexio_read_ecp_power(trexio_t* const file, int32_t* const ecp_power);
trexio_exit_code trexio_write_ecp_power(trexio_t* const file, const int32_t* ecp_power);
trexio_exit_code trexio_read_ecp_power_32(trexio_t* const file, int32_t* const ecp_power);
trexio_exit_code trexio_write_ecp_power_32(trexio_t* const file, const int32_t* ecp_power);
trexio_exit_code trexio_read_ecp_power_64(trexio_t* const file, int64_t* const ecp_power);
trexio_exit_code trexio_write_ecp_power_64(trexio_t* const file, const int64_t* ecp_power);
trexio_exit_code trexio_read_safe_ecp_power(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_power(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ecp_power_32(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_power_32(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ecp_power_64(trexio_t* const file, int64_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ecp_power_64(trexio_t* const file, const int64_t* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_basis_nucleus_index(trexio_t* const file);
trexio_exit_code trexio_read_basis_nucleus_index(trexio_t* const file, int32_t* const basis_nucleus_index);
trexio_exit_code trexio_write_basis_nucleus_index(trexio_t* const file, const int32_t* basis_nucleus_index);
trexio_exit_code trexio_read_basis_nucleus_index_32(trexio_t* const file, int32_t* const basis_nucleus_index);
trexio_exit_code trexio_write_basis_nucleus_index_32(trexio_t* const file, const int32_t* basis_nucleus_index);
trexio_exit_code trexio_read_basis_nucleus_index_64(trexio_t* const file, int64_t* const basis_nucleus_index);
trexio_exit_code trexio_write_basis_nucleus_index_64(trexio_t* const file, const int64_t* basis_nucleus_index);
trexio_exit_code trexio_read_safe_basis_nucleus_index(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_nucleus_index(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_basis_nucleus_index_32(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_nucleus_index_32(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_basis_nucleus_index_64(trexio_t* const file, int64_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_nucleus_index_64(trexio_t* const file, const int64_t* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_basis_shell_ang_mom(trexio_t* const file);
trexio_exit_code trexio_read_basis_shell_ang_mom(trexio_t* const file, int32_t* const basis_shell_ang_mom);
trexio_exit_code trexio_write_basis_shell_ang_mom(trexio_t* const file, const int32_t* basis_shell_ang_mom);
trexio_exit_code trexio_read_basis_shell_ang_mom_32(trexio_t* const file, int32_t* const basis_shell_ang_mom);
trexio_exit_code trexio_write_basis_shell_ang_mom_32(trexio_t* const file, const int32_t* basis_shell_ang_mom);
trexio_exit_code trexio_read_basis_shell_ang_mom_64(trexio_t* const file, int64_t* const basis_shell_ang_mom);
trexio_exit_code trexio_write_basis_shell_ang_mom_64(trexio_t* const file, const int64_t* basis_shell_ang_mom);
trexio_exit_code trexio_read_safe_basis_shell_ang_mom(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_shell_ang_mom(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_basis_shell_ang_mom_32(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_shell_ang_mom_32(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_basis_shell_ang_mom_64(trexio_t* const file, int64_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_shell_ang_mom_64(trexio_t* const file, const int64_t* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_basis_shell_factor(trexio_t* const file);
trexio_exit_code trexio_read_basis_shell_factor(trexio_t* const file, double* const basis_shell_factor);
trexio_exit_code trexio_write_basis_shell_factor(trexio_t* const file, const double* basis_shell_factor);
trexio_exit_code trexio_read_basis_shell_factor_32(trexio_t* const file, float* const basis_shell_factor);
trexio_exit_code trexio_write_basis_shell_factor_32(trexio_t* const file, const float* basis_shell_factor);
trexio_exit_code trexio_read_basis_shell_factor_64(trexio_t* const file, double* const basis_shell_factor);
trexio_exit_code trexio_write_basis_shell_factor_64(trexio_t* const file, const double* basis_shell_factor);
trexio_exit_code trexio_read_safe_basis_shell_factor(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_shell_factor(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_basis_shell_factor_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_shell_factor_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_basis_shell_factor_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_shell_factor_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_basis_shell_index(trexio_t* const file);
trexio_exit_code trexio_read_basis_shell_index(trexio_t* const file, int32_t* const basis_shell_index);
trexio_exit_code trexio_write_basis_shell_index(trexio_t* const file, const int32_t* basis_shell_index);
trexio_exit_code trexio_read_basis_shell_index_32(trexio_t* const file, int32_t* const basis_shell_index);
trexio_exit_code trexio_write_basis_shell_index_32(trexio_t* const file, const int32_t* basis_shell_index);
trexio_exit_code trexio_read_basis_shell_index_64(trexio_t* const file, int64_t* const basis_shell_index);
trexio_exit_code trexio_write_basis_shell_index_64(trexio_t* const file, const int64_t* basis_shell_index);
trexio_exit_code trexio_read_safe_basis_shell_index(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_shell_index(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_basis_shell_index_32(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_shell_index_32(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_basis_shell_index_64(trexio_t* const file, int64_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_shell_index_64(trexio_t* const file, const int64_t* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_basis_exponent(trexio_t* const file);
trexio_exit_code trexio_read_basis_exponent(trexio_t* const file, double* const basis_exponent);
trexio_exit_code trexio_write_basis_exponent(trexio_t* const file, const double* basis_exponent);
trexio_exit_code trexio_read_basis_exponent_32(trexio_t* const file, float* const basis_exponent);
trexio_exit_code trexio_write_basis_exponent_32(trexio_t* const file, const float* basis_exponent);
trexio_exit_code trexio_read_basis_exponent_64(trexio_t* const file, double* const basis_exponent);
trexio_exit_code trexio_write_basis_exponent_64(trexio_t* const file, const double* basis_exponent);
trexio_exit_code trexio_read_safe_basis_exponent(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_exponent(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_basis_exponent_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_exponent_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_basis_exponent_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_exponent_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_basis_coefficient(trexio_t* const file);
trexio_exit_code trexio_read_basis_coefficient(trexio_t* const file, double* const basis_coefficient);
trexio_exit_code trexio_write_basis_coefficient(trexio_t* const file, const double* basis_coefficient);
trexio_exit_code trexio_read_basis_coefficient_32(trexio_t* const file, float* const basis_coefficient);
trexio_exit_code trexio_write_basis_coefficient_32(trexio_t* const file, const float* basis_coefficient);
trexio_exit_code trexio_read_basis_coefficient_64(trexio_t* const file, double* const basis_coefficient);
trexio_exit_code trexio_write_basis_coefficient_64(trexio_t* const file, const double* basis_coefficient);
trexio_exit_code trexio_read_safe_basis_coefficient(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_coefficient(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_basis_coefficient_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_coefficient_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_basis_coefficient_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_coefficient_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_basis_prim_factor(trexio_t* const file);
trexio_exit_code trexio_read_basis_prim_factor(trexio_t* const file, double* const basis_prim_factor);
trexio_exit_code trexio_write_basis_prim_factor(trexio_t* const file, const double* basis_prim_factor);
trexio_exit_code trexio_read_basis_prim_factor_32(trexio_t* const file, float* const basis_prim_factor);
trexio_exit_code trexio_write_basis_prim_factor_32(trexio_t* const file, const float* basis_prim_factor);
trexio_exit_code trexio_read_basis_prim_factor_64(trexio_t* const file, double* const basis_prim_factor);
trexio_exit_code trexio_write_basis_prim_factor_64(trexio_t* const file, const double* basis_prim_factor);
trexio_exit_code trexio_read_safe_basis_prim_factor(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_prim_factor(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_basis_prim_factor_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_prim_factor_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_basis_prim_factor_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_basis_prim_factor_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ao_shell(trexio_t* const file);
trexio_exit_code trexio_read_ao_shell(trexio_t* const file, int32_t* const ao_shell);
trexio_exit_code trexio_write_ao_shell(trexio_t* const file, const int32_t* ao_shell);
trexio_exit_code trexio_read_ao_shell_32(trexio_t* const file, int32_t* const ao_shell);
trexio_exit_code trexio_write_ao_shell_32(trexio_t* const file, const int32_t* ao_shell);
trexio_exit_code trexio_read_ao_shell_64(trexio_t* const file, int64_t* const ao_shell);
trexio_exit_code trexio_write_ao_shell_64(trexio_t* const file, const int64_t* ao_shell);
trexio_exit_code trexio_read_safe_ao_shell(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_shell(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_shell_32(trexio_t* const file, int32_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_shell_32(trexio_t* const file, const int32_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_shell_64(trexio_t* const file, int64_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_shell_64(trexio_t* const file, const int64_t* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ao_normalization(trexio_t* const file);
trexio_exit_code trexio_read_ao_normalization(trexio_t* const file, double* const ao_normalization);
trexio_exit_code trexio_write_ao_normalization(trexio_t* const file, const double* ao_normalization);
trexio_exit_code trexio_read_ao_normalization_32(trexio_t* const file, float* const ao_normalization);
trexio_exit_code trexio_write_ao_normalization_32(trexio_t* const file, const float* ao_normalization);
trexio_exit_code trexio_read_ao_normalization_64(trexio_t* const file, double* const ao_normalization);
trexio_exit_code trexio_write_ao_normalization_64(trexio_t* const file, const double* ao_normalization);
trexio_exit_code trexio_read_safe_ao_normalization(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_normalization(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_normalization_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_normalization_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_normalization_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_normalization_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ao_1e_int_overlap(trexio_t* const file);
trexio_exit_code trexio_read_ao_1e_int_overlap(trexio_t* const file, double* const ao_1e_int_overlap);
trexio_exit_code trexio_write_ao_1e_int_overlap(trexio_t* const file, const double* ao_1e_int_overlap);
trexio_exit_code trexio_read_ao_1e_int_overlap_32(trexio_t* const file, float* const ao_1e_int_overlap);
trexio_exit_code trexio_write_ao_1e_int_overlap_32(trexio_t* const file, const float* ao_1e_int_overlap);
trexio_exit_code trexio_read_ao_1e_int_overlap_64(trexio_t* const file, double* const ao_1e_int_overlap);
trexio_exit_code trexio_write_ao_1e_int_overlap_64(trexio_t* const file, const double* ao_1e_int_overlap);
trexio_exit_code trexio_read_safe_ao_1e_int_overlap(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_overlap(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_overlap_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_overlap_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_overlap_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_overlap_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ao_1e_int_kinetic(trexio_t* const file);
trexio_exit_code trexio_read_ao_1e_int_kinetic(trexio_t* const file, double* const ao_1e_int_kinetic);
trexio_exit_code trexio_write_ao_1e_int_kinetic(trexio_t* const file, const double* ao_1e_int_kinetic);
trexio_exit_code trexio_read_ao_1e_int_kinetic_32(trexio_t* const file, float* const ao_1e_int_kinetic);
trexio_exit_code trexio_write_ao_1e_int_kinetic_32(trexio_t* const file, const float* ao_1e_int_kinetic);
trexio_exit_code trexio_read_ao_1e_int_kinetic_64(trexio_t* const file, double* const ao_1e_int_kinetic);
trexio_exit_code trexio_write_ao_1e_int_kinetic_64(trexio_t* const file, const double* ao_1e_int_kinetic);
trexio_exit_code trexio_read_safe_ao_1e_int_kinetic(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_kinetic(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_kinetic_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_kinetic_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_kinetic_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_kinetic_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ao_1e_int_potential_n_e(trexio_t* const file);
trexio_exit_code trexio_read_ao_1e_int_potential_n_e(trexio_t* const file, double* const ao_1e_int_potential_n_e);
trexio_exit_code trexio_write_ao_1e_int_potential_n_e(trexio_t* const file, const double* ao_1e_int_potential_n_e);
trexio_exit_code trexio_read_ao_1e_int_potential_n_e_32(trexio_t* const file, float* const ao_1e_int_potential_n_e);
trexio_exit_code trexio_write_ao_1e_int_potential_n_e_32(trexio_t* const file, const float* ao_1e_int_potential_n_e);
trexio_exit_code trexio_read_ao_1e_int_potential_n_e_64(trexio_t* const file, double* const ao_1e_int_potential_n_e);
trexio_exit_code trexio_write_ao_1e_int_potential_n_e_64(trexio_t* const file, const double* ao_1e_int_potential_n_e);
trexio_exit_code trexio_read_safe_ao_1e_int_potential_n_e(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_potential_n_e(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_potential_n_e_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_potential_n_e_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_potential_n_e_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_potential_n_e_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ao_1e_int_ecp(trexio_t* const file);
trexio_exit_code trexio_read_ao_1e_int_ecp(trexio_t* const file, double* const ao_1e_int_ecp);
trexio_exit_code trexio_write_ao_1e_int_ecp(trexio_t* const file, const double* ao_1e_int_ecp);
trexio_exit_code trexio_read_ao_1e_int_ecp_32(trexio_t* const file, float* const ao_1e_int_ecp);
trexio_exit_code trexio_write_ao_1e_int_ecp_32(trexio_t* const file, const float* ao_1e_int_ecp);
trexio_exit_code trexio_read_ao_1e_int_ecp_64(trexio_t* const file, double* const ao_1e_int_ecp);
trexio_exit_code trexio_write_ao_1e_int_ecp_64(trexio_t* const file, const double* ao_1e_int_ecp);
trexio_exit_code trexio_read_safe_ao_1e_int_ecp(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_ecp(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_ecp_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_ecp_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_ecp_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_ecp_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ao_1e_int_core_hamiltonian(trexio_t* const file);
trexio_exit_code trexio_read_ao_1e_int_core_hamiltonian(trexio_t* const file, double* const ao_1e_int_core_hamiltonian);
trexio_exit_code trexio_write_ao_1e_int_core_hamiltonian(trexio_t* const file, const double* ao_1e_int_core_hamiltonian);
trexio_exit_code trexio_read_ao_1e_int_core_hamiltonian_32(trexio_t* const file, float* const ao_1e_int_core_hamiltonian);
trexio_exit_code trexio_write_ao_1e_int_core_hamiltonian_32(trexio_t* const file, const float* ao_1e_int_core_hamiltonian);
trexio_exit_code trexio_read_ao_1e_int_core_hamiltonian_64(trexio_t* const file, double* const ao_1e_int_core_hamiltonian);
trexio_exit_code trexio_write_ao_1e_int_core_hamiltonian_64(trexio_t* const file, const double* ao_1e_int_core_hamiltonian);
trexio_exit_code trexio_read_safe_ao_1e_int_core_hamiltonian(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_core_hamiltonian(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_core_hamiltonian_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_core_hamiltonian_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_core_hamiltonian_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_core_hamiltonian_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ao_1e_int_overlap_im(trexio_t* const file);
trexio_exit_code trexio_read_ao_1e_int_overlap_im(trexio_t* const file, double* const ao_1e_int_overlap_im);
trexio_exit_code trexio_write_ao_1e_int_overlap_im(trexio_t* const file, const double* ao_1e_int_overlap_im);
trexio_exit_code trexio_read_ao_1e_int_overlap_im_32(trexio_t* const file, float* const ao_1e_int_overlap_im);
trexio_exit_code trexio_write_ao_1e_int_overlap_im_32(trexio_t* const file, const float* ao_1e_int_overlap_im);
trexio_exit_code trexio_read_ao_1e_int_overlap_im_64(trexio_t* const file, double* const ao_1e_int_overlap_im);
trexio_exit_code trexio_write_ao_1e_int_overlap_im_64(trexio_t* const file, const double* ao_1e_int_overlap_im);
trexio_exit_code trexio_read_safe_ao_1e_int_overlap_im(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_overlap_im(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_overlap_im_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_overlap_im_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_overlap_im_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_overlap_im_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ao_1e_int_kinetic_im(trexio_t* const file);
trexio_exit_code trexio_read_ao_1e_int_kinetic_im(trexio_t* const file, double* const ao_1e_int_kinetic_im);
trexio_exit_code trexio_write_ao_1e_int_kinetic_im(trexio_t* const file, const double* ao_1e_int_kinetic_im);
trexio_exit_code trexio_read_ao_1e_int_kinetic_im_32(trexio_t* const file, float* const ao_1e_int_kinetic_im);
trexio_exit_code trexio_write_ao_1e_int_kinetic_im_32(trexio_t* const file, const float* ao_1e_int_kinetic_im);
trexio_exit_code trexio_read_ao_1e_int_kinetic_im_64(trexio_t* const file, double* const ao_1e_int_kinetic_im);
trexio_exit_code trexio_write_ao_1e_int_kinetic_im_64(trexio_t* const file, const double* ao_1e_int_kinetic_im);
trexio_exit_code trexio_read_safe_ao_1e_int_kinetic_im(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_kinetic_im(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_kinetic_im_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_kinetic_im_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_kinetic_im_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_kinetic_im_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ao_1e_int_potential_n_e_im(trexio_t* const file);
trexio_exit_code trexio_read_ao_1e_int_potential_n_e_im(trexio_t* const file, double* const ao_1e_int_potential_n_e_im);
trexio_exit_code trexio_write_ao_1e_int_potential_n_e_im(trexio_t* const file, const double* ao_1e_int_potential_n_e_im);
trexio_exit_code trexio_read_ao_1e_int_potential_n_e_im_32(trexio_t* const file, float* const ao_1e_int_potential_n_e_im);
trexio_exit_code trexio_write_ao_1e_int_potential_n_e_im_32(trexio_t* const file, const float* ao_1e_int_potential_n_e_im);
trexio_exit_code trexio_read_ao_1e_int_potential_n_e_im_64(trexio_t* const file, double* const ao_1e_int_potential_n_e_im);
trexio_exit_code trexio_write_ao_1e_int_potential_n_e_im_64(trexio_t* const file, const double* ao_1e_int_potential_n_e_im);
trexio_exit_code trexio_read_safe_ao_1e_int_potential_n_e_im(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_potential_n_e_im(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_potential_n_e_im_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_potential_n_e_im_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_potential_n_e_im_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_potential_n_e_im_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ao_1e_int_ecp_im(trexio_t* const file);
trexio_exit_code trexio_read_ao_1e_int_ecp_im(trexio_t* const file, double* const ao_1e_int_ecp_im);
trexio_exit_code trexio_write_ao_1e_int_ecp_im(trexio_t* const file, const double* ao_1e_int_ecp_im);
trexio_exit_code trexio_read_ao_1e_int_ecp_im_32(trexio_t* const file, float* const ao_1e_int_ecp_im);
trexio_exit_code trexio_write_ao_1e_int_ecp_im_32(trexio_t* const file, const float* ao_1e_int_ecp_im);
trexio_exit_code trexio_read_ao_1e_int_ecp_im_64(trexio_t* const file, double* const ao_1e_int_ecp_im);
trexio_exit_code trexio_write_ao_1e_int_ecp_im_64(trexio_t* const file, const double* ao_1e_int_ecp_im);
trexio_exit_code trexio_read_safe_ao_1e_int_ecp_im(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_ecp_im(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_ecp_im_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_ecp_im_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_ecp_im_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_ecp_im_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ao_1e_int_core_hamiltonian_im(trexio_t* const file);
trexio_exit_code trexio_read_ao_1e_int_core_hamiltonian_im(trexio_t* const file, double* const ao_1e_int_core_hamiltonian_im);
trexio_exit_code trexio_write_ao_1e_int_core_hamiltonian_im(trexio_t* const file, const double* ao_1e_int_core_hamiltonian_im);
trexio_exit_code trexio_read_ao_1e_int_core_hamiltonian_im_32(trexio_t* const file, float* const ao_1e_int_core_hamiltonian_im);
trexio_exit_code trexio_write_ao_1e_int_core_hamiltonian_im_32(trexio_t* const file, const float* ao_1e_int_core_hamiltonian_im);
trexio_exit_code trexio_read_ao_1e_int_core_hamiltonian_im_64(trexio_t* const file, double* const ao_1e_int_core_hamiltonian_im);
trexio_exit_code trexio_write_ao_1e_int_core_hamiltonian_im_64(trexio_t* const file, const double* ao_1e_int_core_hamiltonian_im);
trexio_exit_code trexio_read_safe_ao_1e_int_core_hamiltonian_im(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_core_hamiltonian_im(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_core_hamiltonian_im_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_core_hamiltonian_im_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_ao_1e_int_core_hamiltonian_im_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_ao_1e_int_core_hamiltonian_im_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_mo_coefficient(trexio_t* const file);
trexio_exit_code trexio_read_mo_coefficient(trexio_t* const file, double* const mo_coefficient);
trexio_exit_code trexio_write_mo_coefficient(trexio_t* const file, const double* mo_coefficient);
trexio_exit_code trexio_read_mo_coefficient_32(trexio_t* const file, float* const mo_coefficient);
trexio_exit_code trexio_write_mo_coefficient_32(trexio_t* const file, const float* mo_coefficient);
trexio_exit_code trexio_read_mo_coefficient_64(trexio_t* const file, double* const mo_coefficient);
trexio_exit_code trexio_write_mo_coefficient_64(trexio_t* const file, const double* mo_coefficient);
trexio_exit_code trexio_read_safe_mo_coefficient(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_coefficient(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_coefficient_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_coefficient_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_coefficient_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_coefficient_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_mo_coefficient_im(trexio_t* const file);
trexio_exit_code trexio_read_mo_coefficient_im(trexio_t* const file, double* const mo_coefficient_im);
trexio_exit_code trexio_write_mo_coefficient_im(trexio_t* const file, const double* mo_coefficient_im);
trexio_exit_code trexio_read_mo_coefficient_im_32(trexio_t* const file, float* const mo_coefficient_im);
trexio_exit_code trexio_write_mo_coefficient_im_32(trexio_t* const file, const float* mo_coefficient_im);
trexio_exit_code trexio_read_mo_coefficient_im_64(trexio_t* const file, double* const mo_coefficient_im);
trexio_exit_code trexio_write_mo_coefficient_im_64(trexio_t* const file, const double* mo_coefficient_im);
trexio_exit_code trexio_read_safe_mo_coefficient_im(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_coefficient_im(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_coefficient_im_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_coefficient_im_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_coefficient_im_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_coefficient_im_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_mo_occupation(trexio_t* const file);
trexio_exit_code trexio_read_mo_occupation(trexio_t* const file, double* const mo_occupation);
trexio_exit_code trexio_write_mo_occupation(trexio_t* const file, const double* mo_occupation);
trexio_exit_code trexio_read_mo_occupation_32(trexio_t* const file, float* const mo_occupation);
trexio_exit_code trexio_write_mo_occupation_32(trexio_t* const file, const float* mo_occupation);
trexio_exit_code trexio_read_mo_occupation_64(trexio_t* const file, double* const mo_occupation);
trexio_exit_code trexio_write_mo_occupation_64(trexio_t* const file, const double* mo_occupation);
trexio_exit_code trexio_read_safe_mo_occupation(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_occupation(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_occupation_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_occupation_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_occupation_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_occupation_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_mo_1e_int_overlap(trexio_t* const file);
trexio_exit_code trexio_read_mo_1e_int_overlap(trexio_t* const file, double* const mo_1e_int_overlap);
trexio_exit_code trexio_write_mo_1e_int_overlap(trexio_t* const file, const double* mo_1e_int_overlap);
trexio_exit_code trexio_read_mo_1e_int_overlap_32(trexio_t* const file, float* const mo_1e_int_overlap);
trexio_exit_code trexio_write_mo_1e_int_overlap_32(trexio_t* const file, const float* mo_1e_int_overlap);
trexio_exit_code trexio_read_mo_1e_int_overlap_64(trexio_t* const file, double* const mo_1e_int_overlap);
trexio_exit_code trexio_write_mo_1e_int_overlap_64(trexio_t* const file, const double* mo_1e_int_overlap);
trexio_exit_code trexio_read_safe_mo_1e_int_overlap(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_overlap(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_overlap_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_overlap_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_overlap_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_overlap_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_mo_1e_int_kinetic(trexio_t* const file);
trexio_exit_code trexio_read_mo_1e_int_kinetic(trexio_t* const file, double* const mo_1e_int_kinetic);
trexio_exit_code trexio_write_mo_1e_int_kinetic(trexio_t* const file, const double* mo_1e_int_kinetic);
trexio_exit_code trexio_read_mo_1e_int_kinetic_32(trexio_t* const file, float* const mo_1e_int_kinetic);
trexio_exit_code trexio_write_mo_1e_int_kinetic_32(trexio_t* const file, const float* mo_1e_int_kinetic);
trexio_exit_code trexio_read_mo_1e_int_kinetic_64(trexio_t* const file, double* const mo_1e_int_kinetic);
trexio_exit_code trexio_write_mo_1e_int_kinetic_64(trexio_t* const file, const double* mo_1e_int_kinetic);
trexio_exit_code trexio_read_safe_mo_1e_int_kinetic(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_kinetic(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_kinetic_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_kinetic_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_kinetic_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_kinetic_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_mo_1e_int_potential_n_e(trexio_t* const file);
trexio_exit_code trexio_read_mo_1e_int_potential_n_e(trexio_t* const file, double* const mo_1e_int_potential_n_e);
trexio_exit_code trexio_write_mo_1e_int_potential_n_e(trexio_t* const file, const double* mo_1e_int_potential_n_e);
trexio_exit_code trexio_read_mo_1e_int_potential_n_e_32(trexio_t* const file, float* const mo_1e_int_potential_n_e);
trexio_exit_code trexio_write_mo_1e_int_potential_n_e_32(trexio_t* const file, const float* mo_1e_int_potential_n_e);
trexio_exit_code trexio_read_mo_1e_int_potential_n_e_64(trexio_t* const file, double* const mo_1e_int_potential_n_e);
trexio_exit_code trexio_write_mo_1e_int_potential_n_e_64(trexio_t* const file, const double* mo_1e_int_potential_n_e);
trexio_exit_code trexio_read_safe_mo_1e_int_potential_n_e(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_potential_n_e(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_potential_n_e_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_potential_n_e_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_potential_n_e_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_potential_n_e_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_mo_1e_int_ecp(trexio_t* const file);
trexio_exit_code trexio_read_mo_1e_int_ecp(trexio_t* const file, double* const mo_1e_int_ecp);
trexio_exit_code trexio_write_mo_1e_int_ecp(trexio_t* const file, const double* mo_1e_int_ecp);
trexio_exit_code trexio_read_mo_1e_int_ecp_32(trexio_t* const file, float* const mo_1e_int_ecp);
trexio_exit_code trexio_write_mo_1e_int_ecp_32(trexio_t* const file, const float* mo_1e_int_ecp);
trexio_exit_code trexio_read_mo_1e_int_ecp_64(trexio_t* const file, double* const mo_1e_int_ecp);
trexio_exit_code trexio_write_mo_1e_int_ecp_64(trexio_t* const file, const double* mo_1e_int_ecp);
trexio_exit_code trexio_read_safe_mo_1e_int_ecp(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_ecp(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_ecp_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_ecp_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_ecp_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_ecp_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_mo_1e_int_core_hamiltonian(trexio_t* const file);
trexio_exit_code trexio_read_mo_1e_int_core_hamiltonian(trexio_t* const file, double* const mo_1e_int_core_hamiltonian);
trexio_exit_code trexio_write_mo_1e_int_core_hamiltonian(trexio_t* const file, const double* mo_1e_int_core_hamiltonian);
trexio_exit_code trexio_read_mo_1e_int_core_hamiltonian_32(trexio_t* const file, float* const mo_1e_int_core_hamiltonian);
trexio_exit_code trexio_write_mo_1e_int_core_hamiltonian_32(trexio_t* const file, const float* mo_1e_int_core_hamiltonian);
trexio_exit_code trexio_read_mo_1e_int_core_hamiltonian_64(trexio_t* const file, double* const mo_1e_int_core_hamiltonian);
trexio_exit_code trexio_write_mo_1e_int_core_hamiltonian_64(trexio_t* const file, const double* mo_1e_int_core_hamiltonian);
trexio_exit_code trexio_read_safe_mo_1e_int_core_hamiltonian(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_core_hamiltonian(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_core_hamiltonian_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_core_hamiltonian_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_core_hamiltonian_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_core_hamiltonian_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_mo_1e_int_overlap_im(trexio_t* const file);
trexio_exit_code trexio_read_mo_1e_int_overlap_im(trexio_t* const file, double* const mo_1e_int_overlap_im);
trexio_exit_code trexio_write_mo_1e_int_overlap_im(trexio_t* const file, const double* mo_1e_int_overlap_im);
trexio_exit_code trexio_read_mo_1e_int_overlap_im_32(trexio_t* const file, float* const mo_1e_int_overlap_im);
trexio_exit_code trexio_write_mo_1e_int_overlap_im_32(trexio_t* const file, const float* mo_1e_int_overlap_im);
trexio_exit_code trexio_read_mo_1e_int_overlap_im_64(trexio_t* const file, double* const mo_1e_int_overlap_im);
trexio_exit_code trexio_write_mo_1e_int_overlap_im_64(trexio_t* const file, const double* mo_1e_int_overlap_im);
trexio_exit_code trexio_read_safe_mo_1e_int_overlap_im(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_overlap_im(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_overlap_im_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_overlap_im_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_overlap_im_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_overlap_im_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_mo_1e_int_kinetic_im(trexio_t* const file);
trexio_exit_code trexio_read_mo_1e_int_kinetic_im(trexio_t* const file, double* const mo_1e_int_kinetic_im);
trexio_exit_code trexio_write_mo_1e_int_kinetic_im(trexio_t* const file, const double* mo_1e_int_kinetic_im);
trexio_exit_code trexio_read_mo_1e_int_kinetic_im_32(trexio_t* const file, float* const mo_1e_int_kinetic_im);
trexio_exit_code trexio_write_mo_1e_int_kinetic_im_32(trexio_t* const file, const float* mo_1e_int_kinetic_im);
trexio_exit_code trexio_read_mo_1e_int_kinetic_im_64(trexio_t* const file, double* const mo_1e_int_kinetic_im);
trexio_exit_code trexio_write_mo_1e_int_kinetic_im_64(trexio_t* const file, const double* mo_1e_int_kinetic_im);
trexio_exit_code trexio_read_safe_mo_1e_int_kinetic_im(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_kinetic_im(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_kinetic_im_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_kinetic_im_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_kinetic_im_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_kinetic_im_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_mo_1e_int_potential_n_e_im(trexio_t* const file);
trexio_exit_code trexio_read_mo_1e_int_potential_n_e_im(trexio_t* const file, double* const mo_1e_int_potential_n_e_im);
trexio_exit_code trexio_write_mo_1e_int_potential_n_e_im(trexio_t* const file, const double* mo_1e_int_potential_n_e_im);
trexio_exit_code trexio_read_mo_1e_int_potential_n_e_im_32(trexio_t* const file, float* const mo_1e_int_potential_n_e_im);
trexio_exit_code trexio_write_mo_1e_int_potential_n_e_im_32(trexio_t* const file, const float* mo_1e_int_potential_n_e_im);
trexio_exit_code trexio_read_mo_1e_int_potential_n_e_im_64(trexio_t* const file, double* const mo_1e_int_potential_n_e_im);
trexio_exit_code trexio_write_mo_1e_int_potential_n_e_im_64(trexio_t* const file, const double* mo_1e_int_potential_n_e_im);
trexio_exit_code trexio_read_safe_mo_1e_int_potential_n_e_im(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_potential_n_e_im(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_potential_n_e_im_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_potential_n_e_im_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_potential_n_e_im_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_potential_n_e_im_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_mo_1e_int_ecp_im(trexio_t* const file);
trexio_exit_code trexio_read_mo_1e_int_ecp_im(trexio_t* const file, double* const mo_1e_int_ecp_im);
trexio_exit_code trexio_write_mo_1e_int_ecp_im(trexio_t* const file, const double* mo_1e_int_ecp_im);
trexio_exit_code trexio_read_mo_1e_int_ecp_im_32(trexio_t* const file, float* const mo_1e_int_ecp_im);
trexio_exit_code trexio_write_mo_1e_int_ecp_im_32(trexio_t* const file, const float* mo_1e_int_ecp_im);
trexio_exit_code trexio_read_mo_1e_int_ecp_im_64(trexio_t* const file, double* const mo_1e_int_ecp_im);
trexio_exit_code trexio_write_mo_1e_int_ecp_im_64(trexio_t* const file, const double* mo_1e_int_ecp_im);
trexio_exit_code trexio_read_safe_mo_1e_int_ecp_im(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_ecp_im(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_ecp_im_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_ecp_im_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_ecp_im_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_ecp_im_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_mo_1e_int_core_hamiltonian_im(trexio_t* const file);
trexio_exit_code trexio_read_mo_1e_int_core_hamiltonian_im(trexio_t* const file, double* const mo_1e_int_core_hamiltonian_im);
trexio_exit_code trexio_write_mo_1e_int_core_hamiltonian_im(trexio_t* const file, const double* mo_1e_int_core_hamiltonian_im);
trexio_exit_code trexio_read_mo_1e_int_core_hamiltonian_im_32(trexio_t* const file, float* const mo_1e_int_core_hamiltonian_im);
trexio_exit_code trexio_write_mo_1e_int_core_hamiltonian_im_32(trexio_t* const file, const float* mo_1e_int_core_hamiltonian_im);
trexio_exit_code trexio_read_mo_1e_int_core_hamiltonian_im_64(trexio_t* const file, double* const mo_1e_int_core_hamiltonian_im);
trexio_exit_code trexio_write_mo_1e_int_core_hamiltonian_im_64(trexio_t* const file, const double* mo_1e_int_core_hamiltonian_im);
trexio_exit_code trexio_read_safe_mo_1e_int_core_hamiltonian_im(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_core_hamiltonian_im(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_core_hamiltonian_im_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_core_hamiltonian_im_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_mo_1e_int_core_hamiltonian_im_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_mo_1e_int_core_hamiltonian_im_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_rdm_1e(trexio_t* const file);
trexio_exit_code trexio_read_rdm_1e(trexio_t* const file, double* const rdm_1e);
trexio_exit_code trexio_write_rdm_1e(trexio_t* const file, const double* rdm_1e);
trexio_exit_code trexio_read_rdm_1e_32(trexio_t* const file, float* const rdm_1e);
trexio_exit_code trexio_write_rdm_1e_32(trexio_t* const file, const float* rdm_1e);
trexio_exit_code trexio_read_rdm_1e_64(trexio_t* const file, double* const rdm_1e);
trexio_exit_code trexio_write_rdm_1e_64(trexio_t* const file, const double* rdm_1e);
trexio_exit_code trexio_read_safe_rdm_1e(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_rdm_1e(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_rdm_1e_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_rdm_1e_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_rdm_1e_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_rdm_1e_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_rdm_1e_up(trexio_t* const file);
trexio_exit_code trexio_read_rdm_1e_up(trexio_t* const file, double* const rdm_1e_up);
trexio_exit_code trexio_write_rdm_1e_up(trexio_t* const file, const double* rdm_1e_up);
trexio_exit_code trexio_read_rdm_1e_up_32(trexio_t* const file, float* const rdm_1e_up);
trexio_exit_code trexio_write_rdm_1e_up_32(trexio_t* const file, const float* rdm_1e_up);
trexio_exit_code trexio_read_rdm_1e_up_64(trexio_t* const file, double* const rdm_1e_up);
trexio_exit_code trexio_write_rdm_1e_up_64(trexio_t* const file, const double* rdm_1e_up);
trexio_exit_code trexio_read_safe_rdm_1e_up(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_rdm_1e_up(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_rdm_1e_up_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_rdm_1e_up_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_rdm_1e_up_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_rdm_1e_up_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_rdm_1e_dn(trexio_t* const file);
trexio_exit_code trexio_read_rdm_1e_dn(trexio_t* const file, double* const rdm_1e_dn);
trexio_exit_code trexio_write_rdm_1e_dn(trexio_t* const file, const double* rdm_1e_dn);
trexio_exit_code trexio_read_rdm_1e_dn_32(trexio_t* const file, float* const rdm_1e_dn);
trexio_exit_code trexio_write_rdm_1e_dn_32(trexio_t* const file, const float* rdm_1e_dn);
trexio_exit_code trexio_read_rdm_1e_dn_64(trexio_t* const file, double* const rdm_1e_dn);
trexio_exit_code trexio_write_rdm_1e_dn_64(trexio_t* const file, const double* rdm_1e_dn);
trexio_exit_code trexio_read_safe_rdm_1e_dn(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_rdm_1e_dn(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_rdm_1e_dn_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_rdm_1e_dn_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_rdm_1e_dn_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_rdm_1e_dn_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_cell_a(trexio_t* const file);
trexio_exit_code trexio_read_cell_a(trexio_t* const file, double* const cell_a);
trexio_exit_code trexio_write_cell_a(trexio_t* const file, const double* cell_a);
trexio_exit_code trexio_read_cell_a_32(trexio_t* const file, float* const cell_a);
trexio_exit_code trexio_write_cell_a_32(trexio_t* const file, const float* cell_a);
trexio_exit_code trexio_read_cell_a_64(trexio_t* const file, double* const cell_a);
trexio_exit_code trexio_write_cell_a_64(trexio_t* const file, const double* cell_a);
trexio_exit_code trexio_read_safe_cell_a(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_cell_a(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_cell_a_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_cell_a_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_cell_a_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_cell_a_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_cell_b(trexio_t* const file);
trexio_exit_code trexio_read_cell_b(trexio_t* const file, double* const cell_b);
trexio_exit_code trexio_write_cell_b(trexio_t* const file, const double* cell_b);
trexio_exit_code trexio_read_cell_b_32(trexio_t* const file, float* const cell_b);
trexio_exit_code trexio_write_cell_b_32(trexio_t* const file, const float* cell_b);
trexio_exit_code trexio_read_cell_b_64(trexio_t* const file, double* const cell_b);
trexio_exit_code trexio_write_cell_b_64(trexio_t* const file, const double* cell_b);
trexio_exit_code trexio_read_safe_cell_b(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_cell_b(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_cell_b_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_cell_b_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_cell_b_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_cell_b_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_cell_c(trexio_t* const file);
trexio_exit_code trexio_read_cell_c(trexio_t* const file, double* const cell_c);
trexio_exit_code trexio_write_cell_c(trexio_t* const file, const double* cell_c);
trexio_exit_code trexio_read_cell_c_32(trexio_t* const file, float* const cell_c);
trexio_exit_code trexio_write_cell_c_32(trexio_t* const file, const float* cell_c);
trexio_exit_code trexio_read_cell_c_64(trexio_t* const file, double* const cell_c);
trexio_exit_code trexio_write_cell_c_64(trexio_t* const file, const double* cell_c);
trexio_exit_code trexio_read_safe_cell_c(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_cell_c(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_cell_c_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_cell_c_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_cell_c_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_cell_c_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_pbc_k_point(trexio_t* const file);
trexio_exit_code trexio_read_pbc_k_point(trexio_t* const file, double* const pbc_k_point);
trexio_exit_code trexio_write_pbc_k_point(trexio_t* const file, const double* pbc_k_point);
trexio_exit_code trexio_read_pbc_k_point_32(trexio_t* const file, float* const pbc_k_point);
trexio_exit_code trexio_write_pbc_k_point_32(trexio_t* const file, const float* pbc_k_point);
trexio_exit_code trexio_read_pbc_k_point_64(trexio_t* const file, double* const pbc_k_point);
trexio_exit_code trexio_write_pbc_k_point_64(trexio_t* const file, const double* pbc_k_point);
trexio_exit_code trexio_read_safe_pbc_k_point(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_pbc_k_point(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_pbc_k_point_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_pbc_k_point_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_pbc_k_point_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_pbc_k_point_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_qmc_point(trexio_t* const file);
trexio_exit_code trexio_read_qmc_point(trexio_t* const file, double* const qmc_point);
trexio_exit_code trexio_write_qmc_point(trexio_t* const file, const double* qmc_point);
trexio_exit_code trexio_read_qmc_point_32(trexio_t* const file, float* const qmc_point);
trexio_exit_code trexio_write_qmc_point_32(trexio_t* const file, const float* qmc_point);
trexio_exit_code trexio_read_qmc_point_64(trexio_t* const file, double* const qmc_point);
trexio_exit_code trexio_write_qmc_point_64(trexio_t* const file, const double* qmc_point);
trexio_exit_code trexio_read_safe_qmc_point(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_qmc_point(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_qmc_point_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_qmc_point_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_qmc_point_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_qmc_point_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_qmc_psi(trexio_t* const file);
trexio_exit_code trexio_read_qmc_psi(trexio_t* const file, double* const qmc_psi);
trexio_exit_code trexio_write_qmc_psi(trexio_t* const file, const double* qmc_psi);
trexio_exit_code trexio_read_qmc_psi_32(trexio_t* const file, float* const qmc_psi);
trexio_exit_code trexio_write_qmc_psi_32(trexio_t* const file, const float* qmc_psi);
trexio_exit_code trexio_read_qmc_psi_64(trexio_t* const file, double* const qmc_psi);
trexio_exit_code trexio_write_qmc_psi_64(trexio_t* const file, const double* qmc_psi);
trexio_exit_code trexio_read_safe_qmc_psi(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_qmc_psi(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_qmc_psi_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_qmc_psi_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_qmc_psi_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_qmc_psi_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_qmc_e_loc(trexio_t* const file);
trexio_exit_code trexio_read_qmc_e_loc(trexio_t* const file, double* const qmc_e_loc);
trexio_exit_code trexio_write_qmc_e_loc(trexio_t* const file, const double* qmc_e_loc);
trexio_exit_code trexio_read_qmc_e_loc_32(trexio_t* const file, float* const qmc_e_loc);
trexio_exit_code trexio_write_qmc_e_loc_32(trexio_t* const file, const float* qmc_e_loc);
trexio_exit_code trexio_read_qmc_e_loc_64(trexio_t* const file, double* const qmc_e_loc);
trexio_exit_code trexio_write_qmc_e_loc_64(trexio_t* const file, const double* qmc_e_loc);
trexio_exit_code trexio_read_safe_qmc_e_loc(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_qmc_e_loc(trexio_t* const file, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_qmc_e_loc_32(trexio_t* const file, float* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_qmc_e_loc_32(trexio_t* const file, const float* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_safe_qmc_e_loc_64(trexio_t* const file, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_safe_qmc_e_loc_64(trexio_t* const file, const double* dset_in, const int64_t dim_in);

trexio_exit_code trexio_has_ao_2e_int_eri(trexio_t* const file);
trexio_exit_code trexio_read_ao_2e_int_eri(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size, int32_t* const index_sparse, double* const value_sparse);
trexio_exit_code trexio_read_ao_2e_int_eri_size(trexio_t* const file, int64_t* const size_max);
trexio_exit_code trexio_write_ao_2e_int_eri(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse, const double* value_sparse);
trexio_exit_code trexio_read_safe_ao_2e_int_eri(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size_read, int32_t* const index_sparse_read, const int64_t size_index_read, double* const value_sparse_read, const int64_t size_value_read);
trexio_exit_code trexio_write_safe_ao_2e_int_eri(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse_write, const int64_t size_index_write, const double* value_sparse_write, const int64_t size_value_write);

trexio_exit_code trexio_has_ao_2e_int_eri_lr(trexio_t* const file);
trexio_exit_code trexio_read_ao_2e_int_eri_lr(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size, int32_t* const index_sparse, double* const value_sparse);
trexio_exit_code trexio_read_ao_2e_int_eri_lr_size(trexio_t* const file, int64_t* const size_max);
trexio_exit_code trexio_write_ao_2e_int_eri_lr(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse, const double* value_sparse);
trexio_exit_code trexio_read_safe_ao_2e_int_eri_lr(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size_read, int32_t* const index_sparse_read, const int64_t size_index_read, double* const value_sparse_read, const int64_t size_value_read);
trexio_exit_code trexio_write_safe_ao_2e_int_eri_lr(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse_write, const int64_t size_index_write, const double* value_sparse_write, const int64_t size_value_write);

trexio_exit_code trexio_has_mo_2e_int_eri(trexio_t* const file);
trexio_exit_code trexio_read_mo_2e_int_eri(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size, int32_t* const index_sparse, double* const value_sparse);
trexio_exit_code trexio_read_mo_2e_int_eri_size(trexio_t* const file, int64_t* const size_max);
trexio_exit_code trexio_write_mo_2e_int_eri(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse, const double* value_sparse);
trexio_exit_code trexio_read_safe_mo_2e_int_eri(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size_read, int32_t* const index_sparse_read, const int64_t size_index_read, double* const value_sparse_read, const int64_t size_value_read);
trexio_exit_code trexio_write_safe_mo_2e_int_eri(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse_write, const int64_t size_index_write, const double* value_sparse_write, const int64_t size_value_write);

trexio_exit_code trexio_has_mo_2e_int_eri_lr(trexio_t* const file);
trexio_exit_code trexio_read_mo_2e_int_eri_lr(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size, int32_t* const index_sparse, double* const value_sparse);
trexio_exit_code trexio_read_mo_2e_int_eri_lr_size(trexio_t* const file, int64_t* const size_max);
trexio_exit_code trexio_write_mo_2e_int_eri_lr(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse, const double* value_sparse);
trexio_exit_code trexio_read_safe_mo_2e_int_eri_lr(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size_read, int32_t* const index_sparse_read, const int64_t size_index_read, double* const value_sparse_read, const int64_t size_value_read);
trexio_exit_code trexio_write_safe_mo_2e_int_eri_lr(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse_write, const int64_t size_index_write, const double* value_sparse_write, const int64_t size_value_write);

trexio_exit_code trexio_has_rdm_2e(trexio_t* const file);
trexio_exit_code trexio_read_rdm_2e(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size, int32_t* const index_sparse, double* const value_sparse);
trexio_exit_code trexio_read_rdm_2e_size(trexio_t* const file, int64_t* const size_max);
trexio_exit_code trexio_write_rdm_2e(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse, const double* value_sparse);
trexio_exit_code trexio_read_safe_rdm_2e(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size_read, int32_t* const index_sparse_read, const int64_t size_index_read, double* const value_sparse_read, const int64_t size_value_read);
trexio_exit_code trexio_write_safe_rdm_2e(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse_write, const int64_t size_index_write, const double* value_sparse_write, const int64_t size_value_write);

trexio_exit_code trexio_has_rdm_2e_upup(trexio_t* const file);
trexio_exit_code trexio_read_rdm_2e_upup(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size, int32_t* const index_sparse, double* const value_sparse);
trexio_exit_code trexio_read_rdm_2e_upup_size(trexio_t* const file, int64_t* const size_max);
trexio_exit_code trexio_write_rdm_2e_upup(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse, const double* value_sparse);
trexio_exit_code trexio_read_safe_rdm_2e_upup(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size_read, int32_t* const index_sparse_read, const int64_t size_index_read, double* const value_sparse_read, const int64_t size_value_read);
trexio_exit_code trexio_write_safe_rdm_2e_upup(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse_write, const int64_t size_index_write, const double* value_sparse_write, const int64_t size_value_write);

trexio_exit_code trexio_has_rdm_2e_dndn(trexio_t* const file);
trexio_exit_code trexio_read_rdm_2e_dndn(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size, int32_t* const index_sparse, double* const value_sparse);
trexio_exit_code trexio_read_rdm_2e_dndn_size(trexio_t* const file, int64_t* const size_max);
trexio_exit_code trexio_write_rdm_2e_dndn(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse, const double* value_sparse);
trexio_exit_code trexio_read_safe_rdm_2e_dndn(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size_read, int32_t* const index_sparse_read, const int64_t size_index_read, double* const value_sparse_read, const int64_t size_value_read);
trexio_exit_code trexio_write_safe_rdm_2e_dndn(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse_write, const int64_t size_index_write, const double* value_sparse_write, const int64_t size_value_write);

trexio_exit_code trexio_has_rdm_2e_updn(trexio_t* const file);
trexio_exit_code trexio_read_rdm_2e_updn(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size, int32_t* const index_sparse, double* const value_sparse);
trexio_exit_code trexio_read_rdm_2e_updn_size(trexio_t* const file, int64_t* const size_max);
trexio_exit_code trexio_write_rdm_2e_updn(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse, const double* value_sparse);
trexio_exit_code trexio_read_safe_rdm_2e_updn(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size_read, int32_t* const index_sparse_read, const int64_t size_index_read, double* const value_sparse_read, const int64_t size_value_read);
trexio_exit_code trexio_write_safe_rdm_2e_updn(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse_write, const int64_t size_index_write, const double* value_sparse_write, const int64_t size_value_write);

trexio_exit_code trexio_has_rdm_2e_dnup(trexio_t* const file);
trexio_exit_code trexio_read_rdm_2e_dnup(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size, int32_t* const index_sparse, double* const value_sparse);
trexio_exit_code trexio_read_rdm_2e_dnup_size(trexio_t* const file, int64_t* const size_max);
trexio_exit_code trexio_write_rdm_2e_dnup(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse, const double* value_sparse);
trexio_exit_code trexio_read_safe_rdm_2e_dnup(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size_read, int32_t* const index_sparse_read, const int64_t size_index_read, double* const value_sparse_read, const int64_t size_value_read);
trexio_exit_code trexio_write_safe_rdm_2e_dnup(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int32_t* index_sparse_write, const int64_t size_index_write, const double* value_sparse_write, const int64_t size_value_write);

trexio_exit_code trexio_has_metadata_code(trexio_t* const file);
trexio_exit_code trexio_read_metadata_code_low(trexio_t* const file, char* dset_out, const int32_t max_str_len);
trexio_exit_code trexio_write_metadata_code_low(trexio_t* const file, char* dset_in, const int32_t max_str_len);
trexio_exit_code trexio_read_metadata_code(trexio_t* const file, char** dset_out, const int32_t max_str_len);
trexio_exit_code trexio_write_metadata_code(trexio_t* const file, const char** dset_in, const int32_t max_str_len);

trexio_exit_code trexio_has_metadata_author(trexio_t* const file);
trexio_exit_code trexio_read_metadata_author_low(trexio_t* const file, char* dset_out, const int32_t max_str_len);
trexio_exit_code trexio_write_metadata_author_low(trexio_t* const file, char* dset_in, const int32_t max_str_len);
trexio_exit_code trexio_read_metadata_author(trexio_t* const file, char** dset_out, const int32_t max_str_len);
trexio_exit_code trexio_write_metadata_author(trexio_t* const file, const char** dset_in, const int32_t max_str_len);

trexio_exit_code trexio_has_nucleus_label(trexio_t* const file);
trexio_exit_code trexio_read_nucleus_label_low(trexio_t* const file, char* dset_out, const int32_t max_str_len);
trexio_exit_code trexio_write_nucleus_label_low(trexio_t* const file, char* dset_in, const int32_t max_str_len);
trexio_exit_code trexio_read_nucleus_label(trexio_t* const file, char** dset_out, const int32_t max_str_len);
trexio_exit_code trexio_write_nucleus_label(trexio_t* const file, const char** dset_in, const int32_t max_str_len);

trexio_exit_code trexio_has_mo_class(trexio_t* const file);
trexio_exit_code trexio_read_mo_class_low(trexio_t* const file, char* dset_out, const int32_t max_str_len);
trexio_exit_code trexio_write_mo_class_low(trexio_t* const file, char* dset_in, const int32_t max_str_len);
trexio_exit_code trexio_read_mo_class(trexio_t* const file, char** dset_out, const int32_t max_str_len);
trexio_exit_code trexio_write_mo_class(trexio_t* const file, const char** dset_in, const int32_t max_str_len);

trexio_exit_code trexio_has_mo_symmetry(trexio_t* const file);
trexio_exit_code trexio_read_mo_symmetry_low(trexio_t* const file, char* dset_out, const int32_t max_str_len);
trexio_exit_code trexio_write_mo_symmetry_low(trexio_t* const file, char* dset_in, const int32_t max_str_len);
trexio_exit_code trexio_read_mo_symmetry(trexio_t* const file, char** dset_out, const int32_t max_str_len);
trexio_exit_code trexio_write_mo_symmetry(trexio_t* const file, const char** dset_in, const int32_t max_str_len);

trexio_exit_code trexio_has_state_label(trexio_t* const file);
trexio_exit_code trexio_read_state_label_low(trexio_t* const file, char* dset_out, const int32_t max_str_len);
trexio_exit_code trexio_write_state_label_low(trexio_t* const file, char* dset_in, const int32_t max_str_len);
trexio_exit_code trexio_read_state_label(trexio_t* const file, char** dset_out, const int32_t max_str_len);
trexio_exit_code trexio_write_state_label(trexio_t* const file, const char** dset_in, const int32_t max_str_len);

trexio_exit_code trexio_has_determinant_list(trexio_t* const file);
trexio_exit_code trexio_has_determinant_coefficient(trexio_t* const file);
trexio_exit_code trexio_read_determinant_list(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size, int64_t* const dset);
trexio_exit_code trexio_read_safe_determinant_list(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size_read, int64_t* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_read_determinant_coefficient(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size, double* const dset);
trexio_exit_code trexio_read_safe_determinant_coefficient(trexio_t* const file, const int64_t offset_file, int64_t* const buffer_size_read, double* const dset_out, const int64_t dim_out);
trexio_exit_code trexio_write_determinant_list(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int64_t* dset);
trexio_exit_code trexio_write_safe_determinant_list(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const int64_t* dset_in, const int64_t dim_in);
trexio_exit_code trexio_write_determinant_coefficient(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const double* dset);
trexio_exit_code trexio_write_safe_determinant_coefficient(trexio_t* const file, const int64_t offset_file, const int64_t buffer_size, const double* dset_in, const int64_t dim_in);
trexio_exit_code trexio_read_determinant_coefficient_size(trexio_t* const file, int64_t* const size_max);
trexio_exit_code trexio_get_int64_num(trexio_t* const file, int32_t* const num);
#endif
